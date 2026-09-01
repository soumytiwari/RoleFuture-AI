from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from sqlalchemy import inspect, text
from app.models import (
    Activity,
    ActivityAssessment,
    Evidence,
    FutureResponsibility,
    Process,
    Role,
    RoleSkill,
    Skill,
)

from app.routes.analysis import router as analysis_router
from app.routes.roles import router as roles_router
from app.routes.rankings import router as rankings_router
from app.routes.compare import router as compare_router
from app.routes.pages import router as pages_router


import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)



def _migrate_small_schema_changes() -> None:
    """Keep the supplied SQLite database compatible with the current models."""
    inspector = inspect(engine)
    role_columns = {column["name"] for column in inspector.get_columns("roles")} if inspector.has_table("roles") else set()
    assessment_columns = {column["name"] for column in inspector.get_columns("activity_assessments")} if inspector.has_table("activity_assessments") else set()

    with engine.begin() as connection:
        if "creation_source" not in role_columns:
            connection.execute(text("ALTER TABLE roles ADD COLUMN creation_source VARCHAR(50) NOT NULL DEFAULT 'researched_seed'"))
        if "assessment_source" not in assessment_columns:
            connection.execute(text("ALTER TABLE activity_assessments ADD COLUMN assessment_source VARCHAR(50) NOT NULL DEFAULT 'researched_seed'"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    _migrate_small_schema_changes()
    yield


app = FastAPI(
    title="RoleFuture AI",
    description="Role-level AI intelligence and future workforce analysis",
    version="0.1.0",
    lifespan=lifespan,
)


app.include_router(analysis_router)
app.include_router(roles_router)
app.include_router(rankings_router)
app.include_router(compare_router)
app.include_router(pages_router)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "application": "RoleFuture AI",
    }
