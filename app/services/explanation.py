import os
from typing import Any

import requests


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


def build_grounded_prompt(role_data: dict[str, Any]) -> str:
    """
    Build a restricted prompt from application-generated facts.

    The model explains the calculated results but does not calculate,
    modify, or reinterpret the numerical scores.
    """

    return f"""
You are an enterprise workforce-analysis assistant.

Explain the likely AI impact on the role using ONLY the structured facts
provided below. Do not invent responsibilities, skills, technologies,
business facts, or statistics. Do not claim that the role will disappear.

The numerical scores were calculated by a transparent Python scoring engine.
Do not change or recalculate any score.

Return a concise explanation with exactly these sections:

1. Overall impact
2. Activities AI may automate
3. Activities AI may augment
4. Human responsibilities that remain important
5. Future skills or responsibilities

Structured application facts:
{role_data}
""".strip()


def fallback_explanation(role_data: dict[str, Any]) -> str:
    """
    Reliable explanation used when Ollama is not installed or unavailable.
    """

    title = role_data.get("role_title", "This role")
    exposure = role_data.get("average_exposure", 0)
    automation = role_data.get("average_automation", 0)
    augmentation = role_data.get("average_augmentation", 0)

    if automation > augmentation:
        impact_summary = (
            "The role contains several activities with repeatable, "
            "structured, or rule-based work that AI may help automate."
        )
    elif augmentation >= automation:
        impact_summary = (
            "The role is more likely to be transformed through AI assistance "
            "than fully automated because human judgment remains important."
        )
    else:
        impact_summary = (
            "The role is likely to experience a combination of automation "
            "and human-AI collaboration."
        )

    return (
        f"{title} has an average AI exposure score of {exposure}/100, "
        f"with average automation potential of {automation}/100 and "
        f"average augmentation potential of {augmentation}/100.\n\n"
        f"{impact_summary}\n\n"
        "The scoring result is based on the structured activities and "
        "assessment factors stored in the application. Human accountability, "
        "professional judgment, exception handling, and stakeholder decisions "
        "remain important wherever they are part of the role."
    )


def generate_explanation(role_data: dict[str, Any]) -> dict[str, Any]:
    """
    Generate a grounded explanation with Ollama.

    If Ollama is unavailable, return the deterministic fallback so the
    application remains usable without an installed local model.
    """

    prompt = build_grounded_prompt(role_data)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                },
            },
            timeout=60,
        )

        response.raise_for_status()
        response_data = response.json()
        explanation = response_data.get("response", "").strip()

        if explanation:
            return {
                "source": "local_ai",
                "model": OLLAMA_MODEL,
                "explanation": explanation,
            }

    except (requests.RequestException, ValueError, KeyError):
        pass

    return {
        "source": "rule_based_fallback",
        "model": None,
        "explanation": fallback_explanation(role_data),
    }
