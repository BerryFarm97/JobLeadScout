from app.database import add_job_lead
from app.job_sources.adzuna import normalize_adzuna_job


def import_adzuna_jobs(raw_jobs, db_path="job_leads.db"):
    imported_count = 0
    for raw_job in raw_jobs:
        normalized_job = normalize_adzuna_job(raw_job)
        lead_added_db = add_job_lead(**normalized_job, db_path=db_path)
        if lead_added_db:
            imported_count += 1
    return imported_count