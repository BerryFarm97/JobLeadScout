import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.database import init_db, get_all_job_leads
from app.services.job_importer import refresh_adzuna_jobs


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_initialized = init_db()
    if not database_initialized:
        raise RuntimeError("Failed to initialize database")
    yield


app = FastAPI(title="Job Lead Scout", lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/job-leads")
def get_job_leads():
    return get_all_job_leads()


@app.post("/job-leads/refresh")
def refresh_job_leads(keywords: str, location: str):
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_key or not app_id:
        raise HTTPException(
            status_code=500,
            detail="Job search credentials are not configured",
        )
    imported_count = refresh_adzuna_jobs(
        app_id=app_id,
        app_key=app_key,
        keywords=keywords,
        location=location,
        results_per_page=10,
    )
    return {"imported_count": imported_count}
