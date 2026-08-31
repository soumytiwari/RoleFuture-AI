"""Role analysis and AI explanation API routes."""

from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models import Role
from app.services.explanation import (
    generate_explanation,
    ollama_status,
)
from app.services.scoring import calculate_role_analysis

router = APIRouter(prefix="/api", tags=["analysis"])


def _build_role_ai_context(db, role: Role) -> dict:
    analysis = calculate_role_analysis(db, role.id)

    activities = []
    automation_count = 0
    augmentation_count = 0
    human_led_count = 0

    for process in role.processes:
        for activity in process.activities:
            assessment = activity.assessment
            if assessment is None:
                continue

            if assessment.impact_type == "Automated":
                automation_count += 1
            elif assessment.impact_type == "Augmented":
                augmentation_count += 1
            else:
                human_led_count += 1

            activities.append(
                {
                    "process": process.name,
                    "activity": activity.name,
                    "description": activity.description,
                    "frequency": activity.frequency,
                    "human_judgment_level": activity.human_judgment_level,
                    "factors": {
                        "repetitiveness": assessment.repetitiveness,
                        "digital_data_availability": assessment.digital_data_availability,
                        "rule_based_potential": assessment.rule_based_potential,
                        "language_intensity": assessment.language_intensity,
                        "human_judgment_requirement": assessment.human_judgment_requirement,
                        "physical_dependency": assessment.physical_dependency,
                        "sensitivity_complexity": assessment.sensitivity_complexity,
                    },
                    "exposure_score": assessment.exposure_score,
                    "exposure_category": assessment.exposure_category,
                    "automation_score": assessment.automation_score,
                    "augmentation_score": assessment.augmentation_score,
                    "impact_type": assessment.impact_type,
                    "reasoning": assessment.reasoning,
                }
            )

    current_skills = []
    future_skills = []
    for role_skill in role.role_skills:
        item = {
            "name": role_skill.skill.name,
            "importance": role_skill.importance,
            "description": role_skill.skill.description,
            "reason": role_skill.reason,
        }
        if role_skill.skill.category.lower() == "future":
            future_skills.append(item)
        else:
            current_skills.append(item)

    future_responsibilities = [
        {
            "responsibility": item.responsibility,
            "description": item.description,
            "priority": item.priority,
        }
        for item in sorted(
            role.future_responsibilities,
            key=lambda item: item.priority,
            reverse=True,
        )
    ]

    return {
        "role_id": role.id,
        "role_title": role.title,
        "department": role.department,
        "industry": role.industry,
        "role_description": role.description,
        "stored_future_profile": role.future_profile,
        "analysis": {
            "activity_count": analysis.activity_count,
            "average_exposure": analysis.average_exposure,
            "average_automation": analysis.average_automation,
            "average_augmentation": analysis.average_augmentation,
            "high_exposure_count": analysis.high_exposure_count,
            "automated_activity_count": automation_count,
            "augmented_activity_count": augmentation_count,
            "human_led_activity_count": human_led_count,
        },
        "current_skills": current_skills,
        "future_skills": future_skills,
        "future_responsibilities": future_responsibilities,
        "activities": activities,
    }


@router.get("/roles/{role_id}/analysis")
def get_role_analysis(role_id: int):
    db = SessionLocal()
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if role is None:
            raise HTTPException(status_code=404, detail="Role not found.")

        try:
            analysis = calculate_role_analysis(db, role_id)
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

        return {
            "role_id": role_id,
            "activity_count": analysis.activity_count,
            "average_exposure": analysis.average_exposure,
            "average_automation": analysis.average_automation,
            "average_augmentation": analysis.average_augmentation,
            "high_exposure_count": analysis.high_exposure_count,
        }
    finally:
        db.close()


@router.get("/roles/{role_id}/explanation")
def get_role_explanation(role_id: int):
    db = SessionLocal()
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if role is None:
            raise HTTPException(status_code=404, detail="Role not found.")

        try:
            role_data = _build_role_ai_context(db, role)
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

        generated = generate_explanation(role_data)

        return {
            "role_id": role.id,
            "role_title": role.title,
            "analysis_facts": role_data,
            **generated,
        }
    finally:
        db.close()


@router.get("/ai/status")
def get_ai_status():
    """Return local model availability without making the main app depend on it."""
    return ollama_status()
