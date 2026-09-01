from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.main import app
from app.services import explanation


client_context = TestClient(app)
client = client_context


def test_health_and_roles_api():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    response = client.get("/api/roles")
    assert response.status_code == 200
    roles = response.json()
    assert len(roles) >= 20
    assert any(role["title"] == "Finance Analyst" for role in roles)


def test_role_detail_contains_current_future_and_activity_data():
    roles = client.get("/api/roles").json()
    finance = next(role for role in roles if role["title"] == "Finance Analyst")

    response = client.get(f"/api/roles/{finance['id']}")
    assert response.status_code == 200
    payload = response.json()

    assert payload["current_skills"]
    assert payload["future_skills"]
    assert payload["future_responsibilities"]
    assert payload["processes"]
    assert payload["analysis"]["activity_count"] > 0
    assert payload["creation_source"] in {"researched_seed", "local_ai", "heuristic_fallback"}

    first_activity = payload["processes"][0]["activities"][0]
    assert first_activity["assessment"]["factors"]["repetitiveness"] in range(1, 6)
    assert 0 <= first_activity["assessment"]["exposure_score"] <= 100


def test_comparison_api_uses_structured_backend_metrics():
    roles = client.get("/api/roles").json()
    finance = next(role for role in roles if role["title"] == "Finance Analyst")
    procurement = next(role for role in roles if role["title"] == "Procurement Analyst")

    response = client.get(
        "/api/compare",
        params={"role_1_id": finance["id"], "role_2_id": procurement["id"]},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["role_1"]["title"] == "Finance Analyst"
    assert payload["role_2"]["title"] == "Procurement Analyst"
    assert "exposure" in payload["differences"]


def test_compare_rejects_same_role():
    response = client.get("/api/compare", params={"role_1_id": 1, "role_2_id": 1})
    assert response.status_code == 400


def test_ai_fallback_is_structured(monkeypatch):
    monkeypatch.setattr(
        explanation,
        "_call_ollama",
        Mock(side_effect=RuntimeError("Ollama unavailable")),
    )

    role_payload = client.get("/api/roles/1").json()
    analysis = client.get("/api/roles/1/analysis").json()

    role_data = {
        "role_id": role_payload["id"],
        "role_title": role_payload["title"],
        "analysis": analysis | {
            "automated_activity_count": 0,
            "augmented_activity_count": 1,
            "human_led_activity_count": 1,
        },
        "activities": [
            {
                "activity": "Test activity",
                "impact_type": "Augmented",
            }
        ],
        "future_skills": role_payload["future_skills"],
        "future_responsibilities": role_payload["future_responsibilities"],
        "stored_future_profile": role_payload["future_profile"],
    }

    result = explanation.generate_explanation(role_data)
    assert result["source"] == "rule_based_fallback"
    assert isinstance(result["explanation"], dict)
    assert "future_role_profile" in result["explanation"]


def test_ai_status_endpoint_returns_contract():
    response = client.get("/api/ai/status")
    assert response.status_code == 200
    payload = response.json()
    assert payload["model"]
    assert "reachable" in payload
    assert "model_available" in payload


def test_ai_success_response_is_structured(monkeypatch):
    monkeypatch.setattr(
        explanation,
        "_call_ollama",
        Mock(return_value=(
            '{"overall_impact":"Mostly augmented.","automated_activities":["Routine reporting"],"augmented_activities":["Analysis"],"human_responsibilities":["Judgment"],"future_skills":["AI-assisted analysis"],"future_role_profile":"AI-enabled analyst.","transformation_drivers":["Structured data"]}',
            "llama3.2:3b",
        )),
    )

    role_payload = client.get("/api/roles/1").json()
    analysis_payload = client.get("/api/roles/1/analysis").json()
    role_data = {
        "role_id": role_payload["id"],
        "role_title": role_payload["title"],
        "analysis": analysis_payload,
        "activities": [],
        "future_skills": role_payload["future_skills"],
        "future_responsibilities": role_payload["future_responsibilities"],
        "stored_future_profile": role_payload["future_profile"],
    }

    result = explanation.generate_explanation(role_data)
    assert result["source"] == "local_ai"
    assert result["model"] == "llama3.2:3b"
    assert result["explanation"]["overall_impact"] == "Mostly augmented."


def test_role_search_is_alphabetical_and_finds_existing_role():
    response = client.get("/api/roles/search", params={"q": "Finance"})
    assert response.status_code == 200
    results = response.json()
    titles = [item["title"] for item in results]
    assert "Finance Analyst" in titles
    assert titles == sorted(titles, key=str.lower)


def test_new_role_can_be_created_and_saved_with_deterministic_fallback(monkeypatch):
    monkeypatch.setattr(
        explanation,
        "_call_ollama",
        Mock(side_effect=RuntimeError("Ollama unavailable")),
    )

    title = "Demo Process Specialist"
    create_response = client.post(
        "/api/roles",
        json={
            "title": title,
            "department": "Operations",
            "description": "Reviews operational records, handles routine requests, investigates exceptions, and supports stakeholders.",
        },
    )
    assert create_response.status_code == 200
    payload = create_response.json()
    assert payload["status"] == "created"
    role_id = payload["role"]["id"]

    detail = client.get(f"/api/roles/{role_id}")
    assert detail.status_code == 200
    role = detail.json()
    assert role["creation_source"] == "heuristic_fallback"
    assert len(role["processes"]) >= 1
    assert len(role["current_skills"]) >= 1
    assert len(role["future_skills"]) >= 1
    assert len(role["future_responsibilities"]) >= 1
    activity = role["processes"][0]["activities"][0]
    assert activity["assessment"]["assessment_source"] == "heuristic_fallback"
    assert all(1 <= value <= 5 for value in activity["assessment"]["factors"].values())

    # Cleanup after the persistence test so the packaged demo database stays unchanged.
    from app.database import SessionLocal
    from app.models import Role
    db = SessionLocal()
    try:
        created = db.query(Role).filter(Role.id == role_id).first()
        db.delete(created)
        db.commit()
    finally:
        db.close()


def test_role_reanalysis_updates_same_role_without_duplicate_and_replaces_generated_content(monkeypatch):
    from app.services import role_builder

    monkeypatch.setattr(
        role_builder,
        "_call_ollama",
        Mock(side_effect=RuntimeError("Ollama unavailable")),
    )

    title = "Reanalysis Demo Specialist"
    first = client.post(
        "/api/roles",
        json={
            "title": title,
            "department": "Operations",
            "description": "Initial description for a role that handles operational requests and records.",
        },
    )
    assert first.status_code == 200
    role_id = first.json()["role"]["id"]

    before = client.get(f"/api/roles/{role_id}").json()
    before_process_count = len(before["processes"])
    before_activity_count = sum(len(process["activities"]) for process in before["processes"])

    second = client.post(
        f"/api/roles/{role_id}/reanalyze",
        json={
            "department": "Customer Operations",
            "description": "Updated description focused on customer requests, workflow coordination, exception handling, and service quality.",
        },
    )
    assert second.status_code == 200
    assert second.json()["status"] == "updated"
    assert second.json()["role"]["id"] == role_id

    after = client.get(f"/api/roles/{role_id}").json()
    assert after["id"] == role_id
    assert after["department"] == "Customer Operations"
    assert after["description"].startswith("Updated description")
    assert len(after["processes"]) == before_process_count
    assert sum(len(process["activities"]) for process in after["processes"]) == before_activity_count
    assert after["creation_source"] == "heuristic_fallback"

    all_matches = client.get("/api/roles/search", params={"q": title}).json()
    assert len([item for item in all_matches if item["title"].lower() == title.lower()]) == 1

    # Cleanup only the role created by this test.
    from app.database import SessionLocal
    from app.models import Role
    db = SessionLocal()
    try:
        created = db.query(Role).filter(Role.id == role_id).first()
        db.delete(created)
        db.commit()
    finally:
        db.close()
