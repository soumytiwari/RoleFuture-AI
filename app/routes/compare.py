from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models import Role
from app.services.comparison import compare_roles as compare_role_data
from app.services.explanation import generate_comparison_explanation

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
        try:
            result = compare_role_data(db, role_1_id, role_2_id)
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="One or both roles were not found.",
            )

        return result
    finally:
        db.close()


@router.get("/compare/explanation")
def compare_explanation(role_1_id: int, role_2_id: int):
    if role_1_id == role_2_id:
        raise HTTPException(
            status_code=400,
            detail="Please select two different roles.",
        )

    db = SessionLocal()
    try:
        comparison = compare_role_data(db, role_1_id, role_2_id)
        if comparison is None:
            raise HTTPException(
                status_code=404,
                detail="One or both roles were not found.",
            )

        return {
            **generate_comparison_explanation(
                {
                    **comparison,
                    "role_1_future_skills": comparison["role_1"]["future_skills"],
                    "role_2_future_skills": comparison["role_2"]["future_skills"],
                }
            ),
            "role_1_id": role_1_id,
            "role_2_id": role_2_id,
        }
    finally:
        db.close()
