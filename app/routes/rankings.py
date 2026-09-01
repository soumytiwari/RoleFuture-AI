from fastapi import APIRouter

from app.database import SessionLocal
from app.models import Role
from app.services.scoring import calculate_role_analysis


router = APIRouter(prefix="/api", tags=["rankings"])


@router.get("/rankings")
def get_rankings():
    db = SessionLocal()

    try:
        roles = db.query(Role).order_by(Role.title).all()
        rankings = []

        for role in roles:
            try:
                analysis = calculate_role_analysis(db, role.id)
            except ValueError:
                continue

            high_exposure_ratio = (
                analysis.high_exposure_count / analysis.activity_count
            )

            role_change_score = (
                0.50 * analysis.average_exposure
                + 0.30 * analysis.average_automation
                + 0.20 * (high_exposure_ratio * 100)
            )

            rankings.append(
                {
                    "role_id": role.id,
                    "title": role.title,
                    "department": role.department,
                    "role_change_score": round(role_change_score, 2),
                    "average_exposure": analysis.average_exposure,
                    "average_automation": analysis.average_automation,
                    "average_augmentation": analysis.average_augmentation,
                    "activity_count": analysis.activity_count,
                    "high_exposure_count": analysis.high_exposure_count,
                }
            )

        rankings.sort(
            key=lambda item: item["role_change_score"],
            reverse=True,
        )

        for position, ranking in enumerate(rankings, start=1):
            ranking["rank"] = position

        return rankings

    finally:
        db.close()
