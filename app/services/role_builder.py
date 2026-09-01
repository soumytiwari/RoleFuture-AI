"""Create structured role intelligence for newly requested roles."""

from __future__ import annotations

import json
import re
from typing import Any

from sqlalchemy.orm import Session

from app.models import (
    Activity,
    ActivityAssessment,
    Evidence,
    FutureResponsibility,
    Process,
    Role,
    RoleSkill,
    Skill,
)
from app.services.explanation import _call_ollama, _extract_json_object, _json_text
from app.services.scoring import analyze_all_assessments, calculate_activity_score


FACTOR_NAMES = [
    "repetitiveness",
    "digital_data_availability",
    "rule_based_potential",
    "language_intensity",
    "human_judgment_requirement",
    "physical_dependency",
    "sensitivity_complexity",
]


ROLE_FAMILY_TEMPLATES = {
    "analyst": {
        "department": "Analysis",
        "processes": [
            ("Data and Information Review", [
                "Collect and validate role-related data",
                "Analyse patterns and exceptions",
                "Prepare an evidence-based analysis",
            ]),
            ("Reporting and Recommendations", [
                "Prepare recurring reports and summaries",
                "Develop recommendations from analysed information",
                "Explain findings to stakeholders",
            ]),
            ("Stakeholder Support", [
                "Respond to stakeholder information requests",
                "Investigate unusual cases",
                "Track follow-up actions and decisions",
            ]),
        ],
    },
    "engineer": {
        "department": "Engineering",
        "processes": [
            ("Design and Development", [
                "Translate requirements into technical solutions",
                "Implement and review technical changes",
                "Test solutions against requirements",
            ]),
            ("Troubleshooting and Improvement", [
                "Investigate technical issues",
                "Analyse logs, measurements, or defects",
                "Recommend and implement improvements",
            ]),
            ("Documentation and Coordination", [
                "Document technical decisions and solutions",
                "Coordinate with technical and business stakeholders",
                "Review work for quality and compliance",
            ]),
        ],
    },
    "manager": {
        "department": "Management",
        "processes": [
            ("Planning and Prioritisation", [
                "Set priorities and allocate resources",
                "Review performance and progress",
                "Plan actions for emerging issues",
            ]),
            ("Team and Stakeholder Management", [
                "Coordinate team activities",
                "Communicate decisions and expectations",
                "Resolve escalated issues",
            ]),
            ("Decision Support", [
                "Review operational information",
                "Evaluate options and trade-offs",
                "Approve or escalate decisions",
            ]),
        ],
    },
    "specialist": {
        "department": "Operations",
        "processes": [
            ("Core Service Delivery", [
                "Process routine role-specific work",
                "Review incoming requests or information",
                "Complete required records and documentation",
            ]),
            ("Quality and Exceptions", [
                "Check work for completeness and quality",
                "Investigate exceptions",
                "Resolve issues or escalate them",
            ]),
            ("Stakeholder Support", [
                "Respond to questions and requests",
                "Coordinate required actions",
                "Communicate outcomes and next steps",
            ]),
        ],
    },
}


def _normalise_factors(raw: Any) -> dict[str, int]:
    result: dict[str, int] = {}
    raw = raw if isinstance(raw, dict) else {}
    for name in FACTOR_NAMES:
        try:
            value = int(round(float(raw.get(name, 3))))
        except (TypeError, ValueError):
            value = 3
        result[name] = max(1, min(5, value))
    return result


def _family_for_title(title: str) -> str:
    lowered = title.lower()
    if any(word in lowered for word in ("engineer", "developer", "architect", "devops")):
        return "engineer"
    if any(word in lowered for word in ("manager", "lead", "supervisor", "head")):
        return "manager"
    if any(word in lowered for word in ("analyst", "researcher", "scientist")):
        return "analyst"
    return "specialist"


def _heuristic_factor(activity_name: str, description: str, title: str) -> dict[str, int]:
    text = f"{activity_name} {description} {title}".lower()

    repetitive = 5 if any(k in text for k in ("routine", "recurring", "collect", "track", "process", "record", "report")) else 3
    digital = 5 if any(k in text for k in ("data", "software", "system", "digital", "report", "document", "database", "code", "log")) else 3
    rule_based = 5 if any(k in text for k in ("validate", "check", "calculate", "process", "rule", "compliance", "record", "test")) else 3
    language = 5 if any(k in text for k in ("report", "document", "communicate", "write", "explain", "review", "request")) else 3
    judgment = 5 if any(k in text for k in ("decide", "strategy", "negotiate", "lead", "manage", "recommend", "investigate", "resolve")) else 3
    physical = 4 if any(k in text for k in ("physical", "equipment", "inspect", "install", "operate", "manual", "onsite")) else 1
    sensitivity = 5 if any(k in text for k in ("employee", "customer", "patient", "legal", "financial", "confidential", "security", "sensitive", "stakeholder")) else 3

    return {
        "repetitiveness": repetitive,
        "digital_data_availability": digital,
        "rule_based_potential": rule_based,
        "language_intensity": language,
        "human_judgment_requirement": judgment,
        "physical_dependency": physical,
        "sensitivity_complexity": sensitivity,
    }


def _fallback_role_payload(title: str, department: str | None, description: str | None) -> dict[str, Any]:
    family = _family_for_title(title)
    template = ROLE_FAMILY_TEMPLATES[family]
    chosen_department = department.strip() if department else template["department"]
    desc = description.strip() if description else (
        f"A {title} role responsible for carrying out its core {family} activities,"
        " reviewing information, solving exceptions, and supporting stakeholders."
    )

    processes = []
    current_skills = ["Role-specific knowledge", "Communication", "Problem solving"]
    future_skills = ["AI-assisted work", "Data literacy", "AI output validation"]
    responsibilities = [
        "Validate AI-assisted outputs",
        "Handle exceptions and decisions requiring human judgment",
        "Monitor the quality of AI-supported workflows",
    ]

    for process_name, activity_names in template["processes"]:
        activities = []
        for name in activity_names:
            factor_values = _heuristic_factor(name, desc, title)
            activities.append(
                {
                    "name": name,
                    "description": f"{name} as part of the {process_name.lower()} process for the {title} role.",
                    "frequency": "Regular",
                    "human_judgment_level": factor_values["human_judgment_requirement"],
                    "factors": factor_values,
                }
            )
        processes.append({"name": process_name, "description": f"Core {process_name.lower()} activities for {title}.", "activities": activities})

    return {
        "department": chosen_department,
        "industry": "Enterprise Services",
        "description": desc,
        "future_profile": f"A future-oriented {title} who combines domain expertise with AI-assisted analysis, workflow oversight, and human judgment.",
        "current_skills": current_skills,
        "future_skills": future_skills,
        "future_responsibilities": responsibilities,
        "processes": processes,
        "generation_source": "heuristic_fallback",
    }


def build_role_prompt(title: str, department: str | None, description: str | None) -> str:
    return f"""
You are creating structured workforce-analysis data for a role requested by a user.

Role title: {title}
Department hint: {department or "not provided"}
User description: {description or "not provided"}

Create a practical, conservative role profile. Do not claim the role will disappear.
Do not use external citations. Do not invent statistics or labour-market forecasts.
Use general occupational knowledge only to describe common responsibilities.

Return ONLY valid JSON with this exact structure:
{{
  "department": "...",
  "industry": "...",
  "description": "...",
  "future_profile": "...",
  "current_skills": ["..."],
  "future_skills": ["..."],
  "future_responsibilities": ["..."],
  "processes": [
    {{
      "name": "...",
      "description": "...",
      "activities": [
        {{
          "name": "...",
          "description": "...",
          "frequency": "Daily|Weekly|Monthly|Quarterly|As needed|Regular",
          "human_judgment_level": 1,
          "factors": {{
            "repetitiveness": 1,
            "digital_data_availability": 1,
            "rule_based_potential": 1,
            "language_intensity": 1,
            "human_judgment_requirement": 1,
            "physical_dependency": 1,
            "sensitivity_complexity": 1
          }}
        }}
      ]
    }}
  ]
}}

Requirements:
- 3 processes.
- 3 activities per process.
- Factor values must be integers from 1 to 5.
- Make activities specific to the supplied role, not generic placeholders.
- Future skills and responsibilities should follow from the activities and AI-impact characteristics.
- Prefer role transformation and augmentation over replacement language.
""".strip()


def _validate_generated_payload(payload: dict[str, Any]) -> dict[str, Any]:
    required_text = ("department", "industry", "description", "future_profile")
    if any(not str(payload.get(key, "")).strip() for key in required_text):
        raise ValueError("Generated role profile is missing required text fields.")

    for key in ("current_skills", "future_skills", "future_responsibilities", "processes"):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"Generated role profile field {key} is invalid.")

    processes = payload["processes"]
    if len(processes) < 1 or any(not isinstance(item, dict) for item in processes):
        raise ValueError("Generated role profile contains no usable processes.")

    for process_payload in processes:
        activities = process_payload.get("activities")
        if not isinstance(activities, list) or not activities:
            raise ValueError("Generated role profile contains a process with no activities.")
        for activity in activities:
            if not isinstance(activity, dict):
                raise ValueError("Generated activity is invalid.")
            factors = activity.get("factors")
            if not isinstance(factors, dict):
                raise ValueError("Generated activity factors are missing.")
            if any(not 1 <= _normalise_factors(factors)[name] <= 5 for name in FACTOR_NAMES):
                raise ValueError("Generated factor values are outside the 1-to-5 range.")

    return payload


def build_role_payload(title: str, department: str | None, description: str | None) -> dict[str, Any]:
    fallback = _fallback_role_payload(title, department, description)
    try:
        text, model = _call_ollama(build_role_prompt(title, department, description))
        parsed = _extract_json_object(text)
        if not parsed:
            raise ValueError("The model did not return a usable role profile.")
        parsed = _validate_generated_payload(parsed)
        return {**fallback, **parsed, "generation_source": "local_ai", "generation_model": model}
    except Exception:
        return fallback


def _clear_role_generated_content(db: Session, role: Role) -> None:
    """Remove generated children while keeping the Role row/id for updates."""
    old_skill_ids = [item.skill_id for item in list(role.role_skills)]
    process_ids = [item.id for item in list(role.processes)]
    activity_ids = [
        activity.id
        for process in list(role.processes)
        for activity in list(process.activities)
    ]

    if activity_ids:
        db.query(Evidence).filter(Evidence.activity_id.in_(activity_ids)).delete(
            synchronize_session=False
        )
        db.query(ActivityAssessment).filter(
            ActivityAssessment.activity_id.in_(activity_ids)
        ).delete(synchronize_session=False)
        db.query(Activity).filter(Activity.id.in_(activity_ids)).delete(
            synchronize_session=False
        )
    if process_ids:
        db.query(Process).filter(Process.id.in_(process_ids)).delete(
            synchronize_session=False
        )

    db.query(FutureResponsibility).filter(
        FutureResponsibility.role_id == role.id
    ).delete(synchronize_session=False)
    db.query(RoleSkill).filter(RoleSkill.role_id == role.id).delete(
        synchronize_session=False
    )

    # Remove role-specific skills that are no longer referenced.
    if old_skill_ids:
        for skill_id in old_skill_ids:
            skill = db.query(Skill).filter(Skill.id == skill_id).first()
            if skill is not None and not db.query(RoleSkill).filter(RoleSkill.skill_id == skill_id).first():
                db.delete(skill)
    db.flush()


def persist_role_payload(
    db: Session,
    title: str,
    payload: dict[str, Any],
    existing_role: Role | None = None,
) -> Role:
    if existing_role is None:
        role = Role(
            title=title.strip(),
            department=str(payload.get("department") or "Operations")[:100],
            industry=str(payload.get("industry") or "Enterprise Services")[:100],
            description=str(payload.get("description") or "")[:5000],
            future_profile=str(payload.get("future_profile") or "")[:5000],
            creation_source=str(payload.get("generation_source") or "heuristic_fallback")[:50],
        )
        db.add(role)
        db.flush()
    else:
        role_id = existing_role.id
        _clear_role_generated_content(db, existing_role)
        db.expunge_all()
        role = db.get(Role, role_id)
        if role is None:
            raise ValueError("Role disappeared while preparing re-analysis.")
        role.title = title.strip()
        role.department = str(payload.get("department") or "Operations")[:100]
        role.industry = str(payload.get("industry") or "Enterprise Services")[:100]
        role.description = str(payload.get("description") or "")[:5000]
        role.future_profile = str(payload.get("future_profile") or "")[:5000]
        role.creation_source = str(payload.get("generation_source") or "heuristic_fallback")[:50]
        db.flush()

    for name in payload.get("current_skills", []):
        skill = Skill(
            name=str(name)[:150],
            category="Current",
            description=f"Current capability relevant to the {role.title} role.",
        )
        db.add(skill)
        db.flush()
        db.add(RoleSkill(role_id=role.id, skill_id=skill.id, importance=4, reason="Generated as part of the role profile."))

    for name in payload.get("future_skills", []):
        skill = Skill(
            name=str(name)[:150],
            category="Future",
            description=f"Future capability relevant to AI-enabled work in the {role.title} role.",
        )
        db.add(skill)
        db.flush()
        db.add(RoleSkill(role_id=role.id, skill_id=skill.id, importance=4, reason="Derived from the role's projected activity changes."))

    for index, responsibility in enumerate(payload.get("future_responsibilities", []), start=1):
        db.add(
            FutureResponsibility(
                role_id=role.id,
                responsibility=str(responsibility)[:250],
                description="Future responsibility generated from the role's activity and AI-impact profile.",
                priority=max(1, 6 - index),
            )
        )

    activity_sources = []
    for process_payload in payload.get("processes", []):
        process = Process(
            role_id=role.id,
            name=str(process_payload.get("name") or "Core Work")[:150],
            description=str(process_payload.get("description") or "Core activities for the role.")[:5000],
        )
        db.add(process)
        db.flush()

        for activity_payload in process_payload.get("activities", []):
            factors = _normalise_factors(activity_payload.get("factors"))
            activity = Activity(
                process_id=process.id,
                name=str(activity_payload.get("name") or "Role activity")[:200],
                description=str(activity_payload.get("description") or "Role-specific work activity.")[:5000],
                frequency=str(activity_payload.get("frequency") or "Regular")[:50],
                human_judgment_level=max(1, min(5, int(activity_payload.get("human_judgment_level", factors["human_judgment_requirement"])))),
            )
            db.add(activity)
            db.flush()
            assessment = ActivityAssessment(
                activity_id=activity.id,
                **factors,
                assessment_source=str(payload.get("generation_source") or "heuristic_fallback")[:50],
            )
            db.add(assessment)
            db.flush()
            result = calculate_activity_score(assessment)
            # Preserve the same deterministic numerical calculation regardless of who supplied the factor values.
            assessment.exposure_score = result.exposure_score
            assessment.automation_score = result.automation_score
            assessment.augmentation_score = result.augmentation_score
            assessment.exposure_category = result.exposure_category
            assessment.impact_type = result.impact_type
            assessment.reasoning = result.reasoning
            activity_sources.append((activity.id, payload.get("generation_source", "heuristic_fallback")))

    db.flush()
    for activity_id, source in activity_sources:
        evidence_type = "AI-generated role profile" if source == "local_ai" else "Heuristic fallback"
        db.add(
            Evidence(
                activity_id=activity_id,
                evidence_type=evidence_type,
                reference_text=(
                    "The role structure and assessment factors were generated from the requested role. "
                    "Numerical exposure, automation, and augmentation scores were calculated by the deterministic scoring engine."
                ),
                source_url=None,
            )
        )

    db.commit()
    db.refresh(role)
    return role
