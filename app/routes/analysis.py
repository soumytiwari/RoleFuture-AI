from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models import Role
from app.services.scoring import calculate_role_analysis


router = APIRouter(prefix="/api", tags=["roles"])


@router.get("/roles")
def get_roles():
    db = SessionLocal()

    try:
        roles = db.query(Role).order_by(Role.title).all()

        return [
            {
                "id": role.id,
                "title": role.title,
                "department": role.department,
                "industry": role.industry,
                "description": role.description,
            }
            for role in roles
        ]

    finally:
        db.close()

@router.get("/roles/{role_id}/analysis")
def get_role_analysis(role_id: int):
    db = SessionLocal()

    try:
        role = db.query(Role).filter(Role.id == role_id).first()

        if role is None:
            raise HTTPException(
                status_code=404,
                detail="Role not found.",
            )

        analysis = calculate_role_analysis(db, role_id)

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
