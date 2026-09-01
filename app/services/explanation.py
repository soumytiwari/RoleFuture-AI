"""Grounded local-LLM explanation service with a deterministic fallback."""

import json
import logging
import os
from typing import Any

import requests

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_URL = os.getenv("OLLAMA_URL", f"{OLLAMA_BASE_URL}/api/generate")
OLLAMA_TAGS_URL = os.getenv("OLLAMA_TAGS_URL", f"{OLLAMA_BASE_URL}/api/tags")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "45"))


def _json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def _extract_json_object(text: str) -> dict[str, Any] | None:
    """Parse plain JSON or JSON wrapped in a markdown code fence."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

    try:
        parsed = json.loads(cleaned)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start >= 0 and end > start:
            try:
                parsed = json.loads(cleaned[start : end + 1])
                return parsed if isinstance(parsed, dict) else None
            except json.JSONDecodeError:
                return None
    return None


def build_grounded_prompt(role_data: dict[str, Any]) -> str:
    return f"""
You are the explanation layer inside an enterprise workforce-analysis application.

The application has already calculated all scores and classifications. You must NOT
calculate new scores, change scores, or invent evidence.

Use ONLY the structured application facts below.

Rules:
- Do not invent facts, responsibilities, skills, technologies, statistics, or sources.
- Do not claim the role will disappear.
- Do not change any numerical value.
- Treat the supplied scoring results as authoritative.
- Separate automation from augmentation.
- Keep human accountability and judgment visible when the supplied data supports it.
- Be concise and business-readable.
- Return ONLY valid JSON. No markdown and no code fences.

Return this exact JSON shape:
{{
  "overall_impact": "...",
  "automated_activities": ["..."],
  "augmented_activities": ["..."],
  "human_responsibilities": ["..."],
  "future_skills": ["..."],
  "future_role_profile": "...",
  "transformation_drivers": ["..."]
}}

Structured application facts:
{_json_text(role_data)}
""".strip()


def build_comparison_prompt(comparison_data: dict[str, Any]) -> str:
    return f"""
You are the explanation layer inside an enterprise workforce-analysis application.

Two roles have already been scored by the application's deterministic analysis engine.
Use ONLY the supplied facts.

Rules:
- Do not invent facts or numbers.
- Do not recalculate or alter scores.
- Do not claim either role will disappear.
- Explain the main differences using the activity evidence supplied.
- Return ONLY valid JSON. No markdown and no code fences.

Return this exact JSON shape:
{{
  "summary": "...",
  "role_1_strengths": ["..."],
  "role_2_strengths": ["..."],
  "main_differences": ["..."],
  "shared_future_skills": ["..."],
  "priority_message": "..."
}}

Structured comparison facts:
{_json_text(comparison_data)}
""".strip()


def fallback_explanation(role_data: dict[str, Any]) -> dict[str, Any]:
    analysis = role_data["analysis"]
    activities = role_data.get("activities", [])

    automated = [
        item["activity"]
        for item in activities
        if item.get("impact_type") == "Automated"
    ]
    augmented = [
        item["activity"]
        for item in activities
        if item.get("impact_type") == "Augmented"
    ]

    drivers = []
    if analysis["average_exposure"] >= 75:
        drivers.append("The role has very high average AI exposure across its analysed activities.")
    elif analysis["average_exposure"] >= 50:
        drivers.append("The role has high average AI exposure across its analysed activities.")
    else:
        drivers.append("The role has a mix of activities with different levels of AI exposure.")

    if automated:
        drivers.append("Some activities have stronger automation potential than augmentation potential.")
    if augmented:
        drivers.append("Several activities are classified as augmented, where AI can assist human work.")

    future_skills = [item["name"] for item in role_data.get("future_skills", [])]
    responsibilities = [
        item["responsibility"] for item in role_data.get("future_responsibilities", [])
    ]

    if analysis["average_augmentation"] >= analysis["average_automation"]:
        summary = (
            f"{role_data['role_title']} is more likely to be transformed through AI assistance "
            "than broad task replacement because the role retains meaningful human judgment."
        )
    else:
        summary = (
            f"{role_data['role_title']} contains a relatively strong set of repeatable or structured "
            "activities that may be suitable for AI-supported automation."
        )

    return {
        "overall_impact": summary,
        "automated_activities": automated,
        "augmented_activities": augmented,
        "human_responsibilities": responsibilities,
        "future_skills": future_skills,
        "future_role_profile": role_data.get("stored_future_profile") or summary,
        "transformation_drivers": drivers,
    }


def ollama_status() -> dict[str, Any]:
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=3)
        response.raise_for_status()
        data = response.json()
        model_names = [item.get("name") for item in data.get("models", [])]
        model_available = any(
            name == OLLAMA_MODEL or (name and name.split(":", 1)[0] == OLLAMA_MODEL.split(":", 1)[0])
            for name in model_names
        )
        return {
            "enabled": True,
            "reachable": True,
            "model": OLLAMA_MODEL,
            "model_available": model_available,
            "available_models": model_names,
        }
    except Exception as exc:
        return {
            "enabled": True,
            "reachable": False,
            "model": OLLAMA_MODEL,
            "model_available": False,
            "available_models": [],
            "error": str(exc),
        }


def _call_ollama(prompt: str) -> tuple[str, str]:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.2},
    }

    logger.info("Calling Ollama model=%s url=%s", OLLAMA_MODEL, OLLAMA_URL)
    response = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT)
    response.raise_for_status()

    response_data = response.json()
    generated_text = response_data.get("response", "").strip()
    if not generated_text:
        raise ValueError("Ollama returned an empty response")

    parsed = _extract_json_object(generated_text)
    if parsed is None:
        raise ValueError("Ollama returned non-JSON explanation content")

    return json.dumps(parsed, ensure_ascii=False), response_data.get("model", OLLAMA_MODEL)


def generate_explanation(role_data: dict[str, Any]) -> dict[str, Any]:
    fallback = fallback_explanation(role_data)
    try:
        generated_json, model = _call_ollama(build_grounded_prompt(role_data))
        generated = _extract_json_object(generated_json)
        if generated is None:
            raise ValueError("Could not parse model response")

        return {
            "source": "local_ai",
            "model": model,
            "explanation": generated,
        }
    except Exception as exc:
        logger.warning("Local AI unavailable; using deterministic fallback: %s", exc)
        return {
            "source": "rule_based_fallback",
            "model": None,
            "explanation": fallback,
            "warning": "Local AI was unavailable, so the application used its deterministic explanation fallback.",
        }


def generate_comparison_explanation(comparison_data: dict[str, Any]) -> dict[str, Any]:
    fallback = _fallback_comparison(comparison_data)
    try:
        generated_json, model = _call_ollama(build_comparison_prompt(comparison_data))
        generated = _extract_json_object(generated_json)
        if generated is None:
            raise ValueError("Could not parse model response")
        return {
            "source": "local_ai",
            "model": model,
            "explanation": generated,
        }
    except Exception as exc:
        logger.warning("Local comparison AI unavailable; using fallback: %s", exc)
        return {
            "source": "rule_based_fallback",
            "model": None,
            "explanation": fallback,
            "warning": "Local AI was unavailable, so the application used its deterministic comparison fallback.",
        }


def _fallback_comparison(comparison_data: dict[str, Any]) -> dict[str, Any]:
    role_1 = comparison_data["role_1"]
    role_2 = comparison_data["role_2"]
    diffs = comparison_data["differences"]

    higher_exposure = role_2["title"] if diffs["exposure"] > 0 else role_1["title"]
    higher_automation = role_2["title"] if diffs["automation"] > 0 else role_1["title"]
    higher_augmentation = role_2["title"] if diffs["augmentation"] > 0 else role_1["title"]

    shared_skills = sorted(
        set(comparison_data.get("role_1_future_skills", []))
        & set(comparison_data.get("role_2_future_skills", []))
    )

    summary = (
        f"{higher_exposure} has the higher average AI exposure by "
        f"{abs(diffs['exposure']):.2f} points."
    )

    return {
        "summary": summary,
        "role_1_strengths": [
            f"Higher augmentation potential than {role_2['title']}." if diffs["augmentation"] < 0 else f"{role_1['title']} has lower augmentation potential than {role_2['title']}."
        ],
        "role_2_strengths": [
            f"Higher automation potential than {role_1['title']}." if diffs["automation"] > 0 else f"{role_2['title']} has lower automation potential than {role_1['title']}."
        ],
        "main_differences": [
            f"{higher_automation} has the higher average automation potential.",
            f"{higher_augmentation} has the higher average augmentation potential.",
        ],
        "shared_future_skills": shared_skills,
        "priority_message": (
            f"Focus first on activities in {higher_exposure} with high exposure and on the future skills "
            "shared by both roles."
        ),
    }
