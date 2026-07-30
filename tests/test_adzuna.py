from unittest.mock import Mock

from app.job_sources.adzuna import fetch_adzuna_jobs, normalize_adzuna_job


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


def test_fetch_adzuna_jobs_returns_results(monkeypatch):
    raw_jobs = [
        {
            "id": "123456",
            "title": "Junior Python Developer",
        }
    ]

    mock_response = Mock()
    mock_response.json.return_value = {"results": raw_jobs}
    mock_get = Mock(return_value=mock_response)

    monkeypatch.setattr(
        "app.job_sources.adzuna.httpx.get",
        mock_get,
    )

    results = fetch_adzuna_jobs(
        app_id="test-app-id",
        app_key="test-app-key",
        keywords="junior python developer",
        location="Houston, TX",
        results_per_page=10,
    )

    assert results == raw_jobs
    mock_response.raise_for_status.assert_called_once_with()
    mock_response.json.assert_called_once_with()
    mock_get.assert_called_once_with(
        "https://api.adzuna.com/v1/api/jobs/us/search/1",
        params={
            "app_id": "test-app-id",
            "app_key": "test-app-key",
            "results_per_page": 10,
            "what": "junior python developer",
            "where": "Houston, TX",
            "content-type": "application/json",
        },
        timeout=10.0,
    )
