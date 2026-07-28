from fastapi import FastAPI

app = FastAPI(title="Job Lead Scout")


@app.get("/health")
def health_check():
    return {"status": "healthy"}
