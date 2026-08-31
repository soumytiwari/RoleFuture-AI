from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models import (
    Activity,
    ActivityAssessment,
    FutureResponsibility,
    Process,
    Role,
    RoleSkill,
)

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
                # "future_profile": role.future_profile,
            }
            for role in roles
        ]

    finally:
        db.close()


@router.get("/roles/{role_id}")
def get_role(role_id: int):
    db = SessionLocal()

    try:
        role = db.query(Role).filter(Role.id == role_id).first()

        if role is None:
            raise HTTPException(
                status_code=404,
                detail=f"Role {role_id} not found",
            )

        role_analysis = calculate_role_analysis(db, role_id)

        processes = (
            db.query(Process)
            .filter(Process.role_id == role_id)
            .order_by(Process.id)
            .all()
        )

        process_data = []

        for process in processes:
            activities = (
                db.query(Activity)
                .filter(Activity.process_id == process.id)
                .order_by(Activity.id)
                .all()
            )

            activity_data = []

            for activity in activities:
                assessment = (
                    db.query(ActivityAssessment)
                    .filter(ActivityAssessment.activity_id == activity.id)
                    .first()
                )

                activity_data.append(
                    {
                        "id": activity.id,
                        "name": activity.name,
                        "description": activity.description,
                        "frequency": activity.frequency,
                        "human_judgment_level": activity.human_judgment_level,
                        "assessment": (
                            {
                                "exposure_score": assessment.exposure_score,
                                "automation_score": assessment.automation_score,
                                "augmentation_score": assessment.augmentation_score,
                                "exposure_category": assessment.exposure_category,
                                "impact_type": assessment.impact_type,
                                "reasoning": assessment.reasoning,
                            }
                            if assessment
                            else None
                        ),
                    }
                )

            process_data.append(
                {
                    "id": process.id,
                    "name": process.name,
                    "description": process.description,
                    "activities": activity_data,
                }
            )

        responsibilities = (
            db.query(FutureResponsibility)
            .filter(FutureResponsibility.role_id == role_id)
            .order_by(FutureResponsibility.priority.desc())
            .all()
        )

        role_skills = (
            db.query(RoleSkill)
            .filter(RoleSkill.role_id == role_id)
            .order_by(RoleSkill.importance.desc())
            .all()
        )

        responsibility_data = [
            {
                "id": responsibility.id,
                "responsibility": responsibility.responsibility,
                "description": responsibility.description,
                "priority": responsibility.priority,
            }
            for responsibility in responsibilities
        ]

        skill_data = [
            {
                "id": role_skill.skill.id,
                "name": role_skill.skill.name,
                "category": role_skill.skill.category,
                "description": role_skill.skill.description,
                "importance": role_skill.importance,
                "reason": role_skill.reason,
            }
            for role_skill in role_skills
        ]


        return {
            "id": role.id,
            "title": role.title,
            "department": role.department,
            "industry": role.industry,
            "description": role.description,
            "future_profile": role.future_profile,
            "future_responsibilities": responsibility_data,
            "future_skills": skill_data,
            "processes": process_data,
            "analysis": {
                "activity_count": role_analysis.activity_count,
                "average_exposure": role_analysis.average_exposure,
                "average_automation": role_analysis.average_automation,
                "average_augmentation": role_analysis.average_augmentation,
                "high_exposure_count": role_analysis.high_exposure_count,
            },
        }

    finally:
        db.close()
