from app.database import Base, SessionLocal, engine
from app.models import (
    Activity, 
    ActivityAssessment, 
    Process, 
    Role,
    FutureResponsibility,
    RoleSkill,
    Skill,
)


def seed_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        existing_role = db.query(Role).first()

        if existing_role:
            print("Database already contains data. Skipping seed.")
            return

        finance_analyst = Role(
            title="Finance Analyst",
            department="Finance",
            industry="Corporate Services",
            description=(
                "Supports financial reporting, budgeting, forecasting, "
                "and business analysis."
            ),
            creation_source="researched_seed",
            future_profile=(
                "A finance professional who combines financial judgement "
                "with AI-assisted analysis and automation oversight."
            ),
        )

        procurement_analyst = Role(
            title="Procurement Analyst",
            department="Procurement",
            industry="Corporate Services",
            description=(
                "Analyses purchasing data, supplier performance, contracts, "
                "and procurement opportunities."
            ),
            future_profile=(
                "A procurement professional who uses AI-assisted supplier "
                "analysis, risk monitoring, and strategic decision-making."
            ),
        )

        db.add_all([finance_analyst, procurement_analyst])
        db.flush()

        finance_responsibilities = [
            FutureResponsibility(
                role_id=finance_analyst.id,
                responsibility="Validate AI-generated financial commentary",
                description=(
                    "Review AI-generated explanations and confirm that they "
                    "accurately reflect the financial data."
                ),
                priority=5,
            ),
            FutureResponsibility(
                role_id=finance_analyst.id,
                responsibility="Interpret AI-detected business risks",
                description=(
                    "Investigate unusual results and use professional judgment "
                    "to assess their business significance."
                ),
                priority=5,
            ),
            FutureResponsibility(
                role_id=finance_analyst.id,
                responsibility="Monitor finance automation workflows",
                description=(
                    "Check that automated reporting and analysis workflows "
                    "produce reliable and controlled results."
                ),
                priority=4,
            ),
        ]

        procurement_responsibilities = [
            FutureResponsibility(
                role_id=procurement_analyst.id,
                responsibility="Monitor AI-assisted supplier analysis",
                description=(
                    "Review supplier insights and identify important changes "
                    "in cost, performance, or risk."
                ),
                priority=5,
            ),
            FutureResponsibility(
                role_id=procurement_analyst.id,
                responsibility="Validate procurement recommendations",
                description=(
                    "Challenge automated recommendations and ensure they "
                    "support commercial and policy requirements."
                ),
                priority=5,
            ),
            FutureResponsibility(
                role_id=procurement_analyst.id,
                responsibility="Manage supplier-risk exceptions",
                description=(
                    "Handle unusual supplier situations that require "
                    "negotiation, judgment, or escalation."
                ),
                priority=4,
            ),
        ]

        finance_skills = [
            Skill(
                name="AI-assisted financial analysis",
                category="Future",
                description=(
                    "Use AI tools to identify patterns, anomalies, and "
                    "insights in financial information."
                ),
            ),
            Skill(
                name="Data governance",
                category="Future",
                description=(
                    "Maintain data quality, controls, traceability, and "
                    "appropriate use of financial data."
                ),
            ),
            Skill(
                name="Scenario modelling",
                category="Future",
                description=(
                    "Evaluate alternative business scenarios using structured "
                    "data and AI-assisted forecasting."
                ),
            ),
        ]

        procurement_skills = [
            Skill(
                name="AI-assisted supplier analysis",
                category="Future",
                description=(
                    "Use AI to compare suppliers, prices, contract terms, "
                    "and performance indicators."
                ),
            ),
            Skill(
                name="Supplier risk monitoring",
                category="Future",
                description=(
                    "Interpret risk signals and monitor changes in supplier "
                    "performance or commercial conditions."
                ),
            ),
            Skill(
                name="Commercial judgment",
                category="Future",
                description=(
                    "Apply business judgment when reviewing automated "
                    "procurement recommendations."
                ),
            ),
        ]

        db.add_all(
            finance_responsibilities
            + procurement_responsibilities
            + finance_skills
            + procurement_skills
        )
        db.flush()

        role_skills = [
            RoleSkill(
                role_id=finance_analyst.id,
                skill_id=finance_skills[0].id,
                importance=5,
                reason=(
                    "Finance analysts will increasingly use AI to support "
                    "analysis and reporting."
                ),
            ),
            RoleSkill(
                role_id=finance_analyst.id,
                skill_id=finance_skills[1].id,
                importance=5,
                reason=(
                    "Reliable financial analysis depends on strong data "
                    "quality and governance."
                ),
            ),
            RoleSkill(
                role_id=finance_analyst.id,
                skill_id=finance_skills[2].id,
                importance=4,
                reason=(
                    "Scenario modelling supports better planning and "
                    "decision-making."
                ),
            ),
            RoleSkill(
                role_id=procurement_analyst.id,
                skill_id=procurement_skills[0].id,
                importance=5,
                reason=(
                    "Supplier comparison is well suited to AI-assisted "
                    "analysis."
                ),
            ),
            RoleSkill(
                role_id=procurement_analyst.id,
                skill_id=procurement_skills[1].id,
                importance=5,
                reason=(
                    "AI can help identify supplier risks, but analysts must "
                    "interpret and investigate them."
                ),
            ),
            RoleSkill(
                role_id=procurement_analyst.id,
                skill_id=procurement_skills[2].id,
                importance=5,
                reason=(
                    "Commercial decisions still require human judgment and "
                    "business context."
                ),
            ),
        ]

        db.add_all(role_skills)


        finance_reporting = Process(
            role_id=finance_analyst.id,
            name="Monthly Reporting",
            description="Preparing regular financial reports for management.",
        )

        finance_forecasting = Process(
            role_id=finance_analyst.id,
            name="Budgeting and Forecasting",
            description="Preparing budgets and financial forecasts.",
        )

        procurement_analysis = Process(
            role_id=procurement_analyst.id,
            name="Supplier Analysis",
            description="Reviewing supplier performance, cost, and risk.",
        )

        procurement_contracts = Process(
            role_id=procurement_analyst.id,
            name="Contract Review",
            description="Reviewing procurement contracts and requirements.",
        )

        db.add_all(
            [
                finance_reporting,
                finance_forecasting,
                procurement_analysis,
                procurement_contracts,
            ]
        )
        db.flush()

        activities = [
            Activity(
                process_id=finance_reporting.id,
                name="Prepare monthly variance report",
                description=(
                    "Compare actual and budget figures and explain "
                    "significant differences."
                ),
                frequency="Monthly",
                human_judgment_level=3,
            ),
            Activity(
                process_id=finance_forecasting.id,
                name="Prepare financial forecast",
                description=(
                    "Use historical results and business assumptions "
                    "to prepare a financial forecast."
                ),
                frequency="Quarterly",
                human_judgment_level=4,
            ),
            Activity(
                process_id=procurement_analysis.id,
                name="Compare supplier prices",
                description=(
                    "Compare supplier prices, terms, and performance "
                    "to identify purchasing opportunities."
                ),
                frequency="Monthly",
                human_judgment_level=2,
            ),
            Activity(
                process_id=procurement_contracts.id,
                name="Review contract requirements",
                description=(
                    "Review contract information and identify important "
                    "commercial requirements and risks."
                ),
                frequency="Per contract",
                human_judgment_level=4,
            ),
        ]

        db.add_all(activities)
        db.flush()

        assessments = [
            ActivityAssessment(
                activity_id=activities[0].id,
                repetitiveness=5,
                digital_data_availability=5,
                rule_based_potential=4,
                language_intensity=4,
                human_judgment_requirement=3,
                physical_dependency=1,
                sensitivity_complexity=3,
            ),
            ActivityAssessment(
                activity_id=activities[1].id,
                repetitiveness=3,
                digital_data_availability=5,
                rule_based_potential=3,
                language_intensity=3,
                human_judgment_requirement=4,
                physical_dependency=1,
                sensitivity_complexity=4,
            ),
            ActivityAssessment(
                activity_id=activities[2].id,
                repetitiveness=4,
                digital_data_availability=5,
                rule_based_potential=5,
                language_intensity=3,
                human_judgment_requirement=2,
                physical_dependency=1,
                sensitivity_complexity=3,
            ),
            ActivityAssessment(
                activity_id=activities[3].id,
                repetitiveness=3,
                digital_data_availability=4,
                rule_based_potential=3,
                language_intensity=5,
                human_judgment_requirement=4,
                physical_dependency=1,
                sensitivity_complexity=5,
            ),
        ]

        db.add_all(assessments)
        db.commit()

        print("Seed data inserted successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
