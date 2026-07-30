from app.database import add_job_lead
from app.job_sources.adzuna import fetch_adzuna_jobs, normalize_adzuna_job


def import_adzuna_jobs(raw_jobs, db_path="job_leads.db"):
    imported_count = 0
    for raw_job in raw_jobs:
        normalized_job = normalize_adzuna_job(raw_job)
        lead_added = add_job_lead(**normalized_job, db_path=db_path)
        if lead_added:
            imported_count += 1
    return imported_count


def refresh_adzuna_jobs(
    app_id, app_key, keywords, location, results_per_page, db_path="job_leads.db"
):
    raw_jobs = fetch_adzuna_jobs(
        app_id=app_id,
        app_key=app_key,
        keywords=keywords,
        location=location,
        results_per_page=results_per_page,
    )

    imported_count = import_adzuna_jobs(raw_jobs, db_path=db_path)

    return imported_count
