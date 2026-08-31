from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models import Role
from app.services.scoring import calculate_role_analysis


router = APIRouter(prefix="/api", tags=["comparison"])


@router.get("/compare")
def compare_roles(role_1_id: int, role_2_id: int):
    if role_1_id == role_2_id:
        raise HTTPException(
            status_code=400,
            detail="Please select two different roles.",
        )

    db = SessionLocal()

    try:
        role_1 = db.query(Role).filter(Role.id == role_1_id).first()
        role_2 = db.query(Role).filter(Role.id == role_2_id).first()

        if role_1 is None or role_2 is None:
            raise HTTPException(
                status_code=404,
                detail="One or both roles were not found.",
            )

        try:
            analysis_1 = calculate_role_analysis(db, role_1.id)
            analysis_2 = calculate_role_analysis(db, role_2.id)
        except ValueError as error:
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )

        exposure_difference = round(
            analysis_2.average_exposure - analysis_1.average_exposure,
            2,
        )

        automation_difference = round(
            analysis_2.average_automation - analysis_1.average_automation,
            2,
        )

        augmentation_difference = round(
            analysis_2.average_augmentation - analysis_1.average_augmentation,
            2,
        )

        return {
            "role_1": {
                "id": role_1.id,
                "title": role_1.title,
                "department": role_1.department,
                "average_exposure": analysis_1.average_exposure,
                "average_automation": analysis_1.average_automation,
                "average_augmentation": analysis_1.average_augmentation,
                "activity_count": analysis_1.activity_count,
                "high_exposure_count": analysis_1.high_exposure_count,
            },
            "role_2": {
                "id": role_2.id,
                "title": role_2.title,
                "department": role_2.department,
                "average_exposure": analysis_2.average_exposure,
                "average_automation": analysis_2.average_automation,
                "average_augmentation": analysis_2.average_augmentation,
                "activity_count": analysis_2.activity_count,
                "high_exposure_count": analysis_2.high_exposure_count,
            },
            "differences": {
                "exposure": exposure_difference,
                "automation": automation_difference,
                "augmentation": augmentation_difference,
            },
        }

    finally:
        db.close()
