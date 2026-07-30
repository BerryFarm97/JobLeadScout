from app.database import get_all_job_leads, init_db
from app.services.job_importer import import_adzuna_jobs


def test_import_adzuna_jobs_saves_each_job(tmp_path):
    db_path = tmp_path / "test_job_leads.db"
    assert init_db(db_path) is True

    raw_jobs = [
        {
            "id": "adzuna-101",
            "title": "Junior Python Developer",
            "redirect_url": "https://example.com/jobs/101",
            "company": {
                "display_name": "Example Company",
            },
            "location": {
                "display_name": "Houston, Texas",
            },
        },
        {
            "id": "adzuna-102",
            "title": "Entry-Level Backend Developer",
            "redirect_url": "https://example.com/jobs/102",
            "company": {
                "display_name": "Another Company",
            },
            "location": {
                "display_name": "Remote",
            },
        },
    ]

    imported_count = import_adzuna_jobs(raw_jobs, db_path=db_path)
    stored_jobs = get_all_job_leads(db_path=db_path)

    assert imported_count == 2
    assert len(stored_jobs) == 2
    assert {job["source_job_id"] for job in stored_jobs} == {
        "adzuna-101",
        "adzuna-102",
    }


def test_import_adzuna_jobs_counts_only_new_jobs(tmp_path):
    db_path = tmp_path / "test_job_leads.db"
    assert init_db(db_path) is True

    raw_job = {
        "id": "adzuna-duplicate",
        "title": "Junior Python Developer",
        "redirect_url": "https://example.com/jobs/duplicate",
        "company": {
            "display_name": "Example Company",
        },
        "location": {
            "display_name": "Remote",
        },
    }

    imported_count = import_adzuna_jobs(
        [raw_job, raw_job],
        db_path=db_path,
    )
    stored_jobs = get_all_job_leads(db_path=db_path)

    assert imported_count == 1
    assert len(stored_jobs) == 1
