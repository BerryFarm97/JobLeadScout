from app.job_sources.adzuna import normalize_adzuna_job


def test_normalize_adzuna_job_maps_required_fields():
    raw_job = {
        "id": "123456",
        "title": "Junior Python Developer",
        "redirect_url": "https://example.com/jobs/123456",
        "company": {
            "display_name": "Example Company",
        },
        "location": {
            "display_name": "Houston, Texas",
        },
        "salary_min": 60000,
        "salary_max": 75000,
        "description": "An entry-level Python development position.",
    }

    expected_job = {
        "source_job_id": "123456",
        "job_source": "Adzuna",
        "company_name": "Example Company",
        "job_title": "Junior Python Developer",
        "url": "https://example.com/jobs/123456",
        "location": "Houston, Texas",
    }

    assert normalize_adzuna_job(raw_job) == expected_job
