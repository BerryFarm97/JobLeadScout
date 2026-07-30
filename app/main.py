from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db, get_all_job_leads


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
