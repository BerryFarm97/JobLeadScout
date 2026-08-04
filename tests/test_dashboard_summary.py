from fastapi.testclient import TestClient

import app.main as main_module


def test_dashboard_displays_total_matching_job_count(monkeypatch):
    def fake_get_job_leads_count(status_filter=None):
        assert status_filter == "saved"
        return 37

    def fake_get_job_leads_page(
        limit,
        offset,
        status_filter=None,
    ):
        assert limit == 20
        assert offset == 0
        assert status_filter == "saved"
        return []

    monkeypatch.setattr(
        main_module,
        "get_job_leads_count",
        fake_get_job_leads_count,
    )
    monkeypatch.setattr(
        main_module,
        "get_job_leads_page",
        fake_get_job_leads_page,
    )

    client = TestClient(main_module.app)
    response = client.get("/", params={"status": "saved"})

    assert response.status_code == 200
    assert "Total Jobs: 37" in response.text
