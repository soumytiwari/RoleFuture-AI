from sqlalchemy.orm import Session

from app.models import Role
from app.services.scoring import calculate_role_analysis


def compare_roles(
    db: Session,
    role_a_id: int,
    role_b_id: int,
) -> dict:
    role_a = db.query(Role).filter(Role.id == role_a_id).first()
    role_b = db.query(Role).filter(Role.id == role_b_id).first()

    if role_a is None or role_b is None:
        return None

    analysis_a = calculate_role_analysis(db, role_a_id)
    analysis_b = calculate_role_analysis(db, role_b_id)

    exposure_difference = round(
        analysis_b["average_exposure"] - analysis_a["average_exposure"],
        2,
    )

    automation_difference = round(
        analysis_b["average_automation"] - analysis_a["average_automation"],
        2,
    )

    augmentation_difference = round(
        analysis_b["average_augmentation"] - analysis_a["average_augmentation"],
        2,
    )

    return {
        "role_a": {
            "id": role_a.id,
            "title": role_a.title,
            "analysis": analysis_a,
        },
        "role_b": {
            "id": role_b.id,
            "title": role_b.title,
            "analysis": analysis_b,
        },
        "differences": {
            "exposure": exposure_difference,
            "automation": automation_difference,
            "augmentation": augmentation_difference,
        },
    }
