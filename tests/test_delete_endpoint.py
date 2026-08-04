from fastapi.testclient import TestClient

import app.main as main_module


def test_delete_archived_job_lead_returns_success(monkeypatch):
    received_job_id = {}

    def fake_delete_job_lead(job_lead_id):
        received_job_id["value"] = job_lead_id
        return True

    monkeypatch.setattr(
        main_module,
        "delete_job_lead",
        fake_delete_job_lead,
    )

    client = TestClient(main_module.app)
    response = client.delete("/job-leads/42")

    assert response.status_code == 200
    assert received_job_id["value"] == 42
    assert response.json() == {
        "job_lead_id": 42,
        "deleted": True,
    }


def test_delete_archived_job_lead_returns_404_on_failure(monkeypatch):
    def fake_delete_job_lead(job_lead_id):
        return False

    monkeypatch.setattr(
        main_module,
        "delete_job_lead",
        fake_delete_job_lead,
    )

    client = TestClient(main_module.app)
    response = client.delete("/job-leads/42")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Archived job lead not found",
    }
