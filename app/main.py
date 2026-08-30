from fastapi import FastAPI

app = FastAPI(
    title="RoleFuture AI",
    description="Role-level AI intelligence and future workforce analysis",
    version="0.1.0",
)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "application": "RoleFuture AI",
    }
