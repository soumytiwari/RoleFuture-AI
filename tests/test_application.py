from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.main import app
from app.services import explanation


client = TestClient(app)


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
