"""Reusable role comparison service."""

from sqlalchemy.orm import Session

from app.models import Role
from app.services.scoring import calculate_role_analysis


def _role_summary(role: Role, analysis) -> dict:
    future_skills = [
        item.skill.name
        for item in role.role_skills
        if item.skill.category.lower() == "future"
    ]
    current_skills = [
        item.skill.name
        for item in role.role_skills
        if item.skill.category.lower() != "future"
    ]

    return {
        "id": role.id,
        "title": role.title,
        "department": role.department,
        "average_exposure": analysis.average_exposure,
        "average_automation": analysis.average_automation,
        "average_augmentation": analysis.average_augmentation,
        "activity_count": analysis.activity_count,
        "high_exposure_count": analysis.high_exposure_count,
        "future_skills": future_skills,
        "current_skills": current_skills,
    }


def compare_roles(db: Session, role_a_id: int, role_b_id: int) -> dict | None:
    role_a = db.query(Role).filter(Role.id == role_a_id).first()
    role_b = db.query(Role).filter(Role.id == role_b_id).first()

    if role_a is None or role_b is None:
        return None

    analysis_a = calculate_role_analysis(db, role_a_id)
    analysis_b = calculate_role_analysis(db, role_b_id)

    summary_a = _role_summary(role_a, analysis_a)
    summary_b = _role_summary(role_b, analysis_b)

    return {
        "role_1": summary_a,
        "role_2": summary_b,
        "differences": {
            "exposure": round(
                analysis_b.average_exposure - analysis_a.average_exposure, 2
            ),
            "automation": round(
                analysis_b.average_automation - analysis_a.average_automation, 2
            ),
            "augmentation": round(
                analysis_b.average_augmentation - analysis_a.average_augmentation, 2
            ),
            "high_exposure_count": (
                analysis_b.high_exposure_count - analysis_a.high_exposure_count
            ),
        },
    }
