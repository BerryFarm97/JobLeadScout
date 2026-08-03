from unittest.mock import Mock


from app.database import get_all_job_leads, init_db
from app.services.job_importer import import_adzuna_jobs, refresh_adzuna_jobs


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
            "salary_min": 60000,
            "salary_max": 75000,
            "description": "An entry-level Python development position.",
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
    stored_job = next(
        job for job in stored_jobs if job["source_job_id"] == "adzuna-101"
    )
    assert stored_job["salary_min"] == 60000
    assert stored_job["salary_max"] == 75000
    assert (
        stored_job["job_description"] == "An entry-level Python development position."
    )


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


def test_refresh_adzuna_jobs_fetches_and_imports(monkeypatch):
    raw_jobs = [{"id": "adzuna-101"}, {"id": "adzuna-102"}]

    mock_fetch = Mock(return_value=raw_jobs)
    mock_import = Mock(return_value=2)

    monkeypatch.setattr(
        "app.services.job_importer.fetch_adzuna_jobs",
        mock_fetch,
    )
    monkeypatch.setattr(
        "app.services.job_importer.import_adzuna_jobs",
        mock_import,
    )

    imported_count = refresh_adzuna_jobs(
        app_id="test-app-id",
        app_key="test-app-key",
        keywords="software developer",
        location="Houston, TX",
        results_per_page=10,
        db_path="test.db",
    )

    assert imported_count == 2
    mock_fetch.assert_called_once_with(
        app_id="test-app-id",
        app_key="test-app-key",
        keywords="software developer",
        location="Houston, TX",
        results_per_page=10,
    )
    mock_import.assert_called_once_with(
        raw_jobs,
        db_path="test.db",
    )
