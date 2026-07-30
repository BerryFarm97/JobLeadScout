from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db


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
