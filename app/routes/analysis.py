from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.services.scoring import calculate_role_analysis

router = APIRouter(prefix="/api", tags=["analysis"])

@router.get("/roles/{role_id}/analysis")
def get_role_analysis(role_id: int):
    db = SessionLocal()

    try:
        try:
            result = calculate_role_analysis(db, role_id)
        except ValueError:
            raise HTTPException(
                status_code = 404,
                detail = f"No analysis found for role {role_id}",
            )

        return {
            "role_id": result.role_id,
            "activity_count": result.activity_count,
            "average_exposure": result.average_exposure,
            "average_automation": result.average_automation,
            "average_augmentation": result.average_augmentation,
            "high_exposure_count": result.high_exposure_count,
        }

    finally:
        db.close()