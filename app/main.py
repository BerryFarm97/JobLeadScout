import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.database import get_all_job_leads, init_db, update_job_lead_status
from app.services.job_importer import refresh_adzuna_jobs

load_dotenv()

STATUS_OPTIONS = ["new", "saved", "applied", "archived"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_initialized = init_db()
    if not database_initialized:
        raise RuntimeError("Failed to initialize database")
    yield


app = FastAPI(title="Job Lead Scout", lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

templates = Jinja2Templates(directory="app/templates")


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


@app.get("/")
def dashboard(request: Request):
    all_job_leads = get_all_job_leads()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"job_leads": all_job_leads},
    )


@app.patch("/job-leads/{job_lead_id}/status")
def change_job_lead_status(job_lead_id: int, new_status: str):
    if new_status not in STATUS_OPTIONS:
        raise HTTPException(
            status_code=400, detail=f"{new_status} is not a valid status"
        )
    status_updated = update_job_lead_status(new_status, job_lead_id)

    if not status_updated:
        raise HTTPException(status_code=404, detail="Job id cannot be found")

    return {
        "job_lead_id": job_lead_id,
        "status": new_status,
    }
