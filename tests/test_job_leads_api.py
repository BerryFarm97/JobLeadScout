from unittest.mock import Mock
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_job_leads_returns_empty_list(monkeypatch): # type: ignore
    mock_get_job_leads = Mock(return_value=[])
    monkeypatch.setattr("app.main.get_all_job_leads", mock_get_job_leads) # type: ignore

    response = client.get("/job-leads")

    assert response.status_code == 200
    assert response.json() == []
    mock_get_job_leads.assert_called_once_with()


def test_get_job_leads_returns_job_leads(monkeypatch): # type: ignore
    sample_job_leads = [ # type: ignore
        {
            "id": 1,
            "company_name": "Test Company",
            "job_title": "Junior Python Developer",
        }
    ]

    mock_get_job_leads = Mock(return_value=sample_job_leads)

    monkeypatch.setattr( # type: ignore
        "app.main.get_all_job_leads",
        mock_get_job_leads,
    )

    response = client.get("/job-leads")

    assert response.status_code == 200
    assert response.json() == sample_job_leads
    mock_get_job_leads.assert_called_once_with()
