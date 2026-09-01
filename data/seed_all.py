"""Create, seed, and analyse the complete RoleFuture AI dataset."""

from app.database import Base, SessionLocal, engine
from app.models import Role, RoleSkill, Skill
from app.services.scoring import analyze_all_assessments
from data.seed import seed_database
from data.seed_additional_roles import seed_additional_roles


BASE_CURRENT_SKILLS = {
    "Finance Analyst": [
        "Financial analysis",
        "Budgeting and forecasting",
        "Spreadsheet modelling",
    ],
    "Procurement Analyst": [
        "Procurement analysis",
        "Supplier evaluation",
        "Contract review",
    ],
}


def _ensure_base_current_skills(db) -> None:
    for role_title, skill_names in BASE_CURRENT_SKILLS.items():
        role = db.query(Role).filter(Role.title == role_title).first()
        if role is None:
            continue

        for skill_name in skill_names:
            skill = db.query(Skill).filter(Skill.name == skill_name, Skill.category == "Current").first()
            if skill is None:
                skill = Skill(
                    name=skill_name,
                    category="Current",
                    description=f"Current capability used by the {role_title.lower()} role.",
                )
                db.add(skill)
                db.flush()

            exists = db.query(RoleSkill).filter(
                RoleSkill.role_id == role.id,
                RoleSkill.skill_id == skill.id,
            ).first()
            if exists is None:
                db.add(
                    RoleSkill(
                        role_id=role.id,
                        skill_id=skill.id,
                        importance=5,
                        reason="This capability is part of the current role profile.",
                    )
                )


def seed_all() -> None:
    Base.metadata.create_all(bind=engine)
    seed_database()
    seed_additional_roles()

    db = SessionLocal()
    try:
        _ensure_base_current_skills(db)
        db.commit()
        assessments = analyze_all_assessments(db)
        role_count = db.query(Role).count()
        print(f"Roles available: {role_count}")
        print(f"Assessments analysed: {len(assessments)}")
        print("RoleFuture AI dataset is ready.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
