from fastapi import APIRouter

from app.database import SessionLocal
from app.models import Role


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
                # "future_profile": role.future_profile,
            }
            for role in roles
        ]

    finally:
        db.close()