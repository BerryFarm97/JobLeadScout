from unittest.mock import Mock
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_job_leads_returns_empty_list(monkeypatch):
    mock_get_job_leads = Mock(return_value=[])
    monkeypatch.setattr("app.main.get_all_job_leads", mock_get_job_leads)

    response = client.get("/job-leads")

    assert response.status_code == 200
    assert response.json() == []
    mock_get_job_leads.assert_called_once_with()


def test_get_job_leads_returns_job_leads(monkeypatch):
    sample_job_leads = [
        {
            "id": 1,
            "company_name": "Test Company",
            "job_title": "Junior Python Developer",
        }
    ]

    mock_get_job_leads = Mock(return_value=sample_job_leads)

    monkeypatch.setattr(
        "app.main.get_all_job_leads",
        mock_get_job_leads,
    )

    response = client.get("/job-leads")

    assert response.status_code == 200
    assert response.json() == sample_job_leads
    mock_get_job_leads.assert_called_once_with()


def test_refresh_job_leads_imports_new_jobs(monkeypatch):
    monkeypatch.setenv("ADZUNA_APP_ID", "test-app-id")
    monkeypatch.setenv("ADZUNA_APP_KEY", "test-app-key")

    mock_refresh = Mock(return_value=3)
    monkeypatch.setattr("app.main.refresh_adzuna_jobs", mock_refresh)

    response = client.post(
        "/job-leads/refresh",
        params={
            "keywords": "software developer",
            "location": "Houston, TX",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"imported_count": 3}
    mock_refresh.assert_called_once_with(
        app_id="test-app-id",
        app_key="test-app-key",
        keywords="software developer",
        location="Houston, TX",
        results_per_page=10,
    )


def test_refresh_job_leads_requires_credentials(monkeypatch):
    monkeypatch.delenv("ADZUNA_APP_ID", raising=False)
    monkeypatch.delenv("ADZUNA_APP_KEY", raising=False)

    response = client.post(
        "/job-leads/refresh",
        params={
            "keywords": "software developer",
            "location": "Houston, TX",
        },
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Job search credentials are not configured"}


def test_change_job_lead_status_updates_existing_job(monkeypatch):
    mock_update_status = Mock(return_value=True)
    monkeypatch.setattr(
        "app.main.update_job_lead_status",
        mock_update_status,
    )

    response = client.patch(
        "/job-leads/72/status",
        params={"new_status": "saved"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "job_lead_id": 72,
        "status": "saved",
    }
    mock_update_status.assert_called_once_with("saved", 72)


def test_change_job_lead_status_rejects_invalid_status(monkeypatch):
    mock_update_status = Mock()
    monkeypatch.setattr(
        "app.main.update_job_lead_status",
        mock_update_status,
    )

    response = client.patch(
        "/job-leads/72/status",
        params={"new_status": "dismissed"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "dismissed is not a valid status"}
    mock_update_status.assert_not_called()


def test_change_job_lead_status_returns_not_found(monkeypatch):
    mock_update_status = Mock(return_value=False)
    monkeypatch.setattr(
        "app.main.update_job_lead_status",
        mock_update_status,
    )

    response = client.patch(
        "/job-leads/999/status",
        params={"new_status": "saved"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Job id cannot be found"}
    mock_update_status.assert_called_once_with("saved", 999)
