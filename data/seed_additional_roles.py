from app.database import Base, SessionLocal, engine

from app.models import (
    Activity,
    ActivityAssessment,
    FutureResponsibility,
    Process,
    Role,
    RoleSkill,
    Skill,
)


ROLE_SPECS = [
    ("Business Analyst", "Business Analysis"),
    ("HR Analyst", "Human Resources"),
    ("Marketing Analyst", "Marketing"),
    ("Operations Analyst", "Operations"),
    ("Risk Analyst", "Risk"),
    ("Compliance Analyst", "Compliance"),
    ("Customer Service Representative", "Customer Service"),
    ("Project Coordinator", "Project Management"),
    ("Supply Chain Planner", "Supply Chain"),
    ("Recruitment Specialist", "Human Resources"),
    ("Payroll Specialist", "Finance"),
    ("Management Accountant", "Finance"),
    ("Internal Auditor", "Audit"),
    ("Contract Administrator", "Legal Operations"),
    ("Credit Analyst", "Finance"),
    ("Research Analyst", "Research"),
    ("Sales Operations Analyst", "Sales"),
    ("Administrative Officer", "Administration"),
]


PROCESS_TEMPLATES = [
    (
        "Data Collection and Review",
        "Collecting, checking, and organizing information used by the role.",
    ),
    (
        "Analysis and Reporting",
        "Analysing information and preparing reports for stakeholders.",
    ),
    (
        "Stakeholder Coordination",
        "Communicating findings and coordinating actions with stakeholders.",
    ),
]


ACTIVITY_TEMPLATES = [
    (
        "Collect and validate operational data",
        "Gather information from business systems, check its quality, and resolve basic inconsistencies.",
        "Weekly",
        2,
    ),
    (
        "Analyse trends and prepare a report",
        "Review structured information, identify patterns, and prepare findings for decision-makers.",
        "Monthly",
        3,
    ),
    (
        "Investigate exceptions and explain findings",
        "Review unusual results, identify possible causes, and communicate recommended actions.",
        "Monthly",
        4,
    ),
]


def get_or_create_skill(db, name, description):
    skill = db.query(Skill).filter(Skill.name == name).first()

    if not skill:
        skill = Skill(
            name=name,
            category="Future",
            description=description,
        )
        db.add(skill)
        db.flush()

    return skill


def seed_additional_roles():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        shared_skills = [
            get_or_create_skill(
                db,
                "AI-assisted analysis",
                "Use AI tools to analyse information, identify patterns, and support recommendations.",
            ),
            get_or_create_skill(
                db,
                "Data literacy and governance",
                "Understand data quality, controls, traceability, and responsible data use.",
            ),
            get_or_create_skill(
                db,
                "Stakeholder communication",
                "Explain findings, challenge outputs, and communicate recommendations clearly.",
            ),
        ]

        inserted_roles = 0
        inserted_activities = 0

        for title, department in ROLE_SPECS:
            existing_role = db.query(Role).filter(Role.title == title).first()

            if existing_role:
                continue

            role = Role(
                title=title,
                department=department,
                industry="Corporate Services",
                description=(
                    f"Supports {department.lower()} processes through data review, "
                    "analysis, reporting, and stakeholder coordination."
                ),
                future_profile=(
                    f"A {title.lower()} who combines professional judgment with "
                    "AI-assisted analysis, automation oversight, and stakeholder communication."
                ),
            )

            db.add(role)
            db.flush()

            for skill_index, skill in enumerate(shared_skills):
                db.add(
                    RoleSkill(
                        role_id=role.id,
                        skill_id=skill.id,
                        importance=5 if skill_index == 0 else 4,
                        reason=(
                            "This capability supports effective use of AI while "
                            "maintaining human review and accountability."
                        ),
                    )
                )

            responsibilities = [
                FutureResponsibility(
                    role_id=role.id,
                    responsibility="Review AI-assisted analysis",
                    description=(
                        "Check AI-supported findings for accuracy, relevance, and business context."
                    ),
                    priority=5,
                ),
                FutureResponsibility(
                    role_id=role.id,
                    responsibility="Manage exceptions and decisions",
                    description=(
                        "Investigate unusual cases and make decisions where human judgment is required."
                    ),
                    priority=5,
                ),
                FutureResponsibility(
                    role_id=role.id,
                    responsibility="Maintain data and process controls",
                    description=(
                        "Help ensure that automated workflows use reliable data and follow business controls."
                    ),
                    priority=4,
                ),
            ]

            db.add_all(responsibilities)

            for process_name, process_description in PROCESS_TEMPLATES:
                process = Process(
                    role_id=role.id,
                    name=process_name,
                    description=process_description,
                )
                db.add(process)
                db.flush()

                for activity_index, activity_data in enumerate(ACTIVITY_TEMPLATES):
                    name, description, frequency, judgment = activity_data

                    activity = Activity(
                        process_id=process.id,
                        name=name,
                        description=description,
                        frequency=frequency,
                        human_judgment_level=judgment,
                    )
                    db.add(activity)
                    db.flush()

                    db.add(
                        ActivityAssessment(
                            activity_id=activity.id,
                            repetitiveness=5 - activity_index,
                            digital_data_availability=5,
                            rule_based_potential=4 - activity_index,
                            language_intensity=3 + activity_index,
                            human_judgment_requirement=judgment,
                            physical_dependency=1,
                            sensitivity_complexity=2 + activity_index,
                        )
                    )

                    inserted_activities += 1

            inserted_roles += 1

        db.commit()

        print(f"Inserted roles: {inserted_roles}")
        print(f"Inserted activities: {inserted_activities}")
        print("Additional role seed completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_additional_roles()
