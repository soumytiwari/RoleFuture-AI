from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="RoleFuture AI",
    description="Role-level AI intelligence and future workforce analysis",
    version="0.1.0",
    lifespan=lifespan,
)


app.include_router(analysis_router)
app.include_router(roles_router)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "application": "RoleFuture AI",
    }
