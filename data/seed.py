from app.database import Base, SessionLocal, engine
from app.models import Activity, ActivityAssessment, Process, Role


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
