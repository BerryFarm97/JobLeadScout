import csv
import io

from fastapi.testclient import TestClient

import app.main as main_module


def make_job_lead(status):
    return {
        "company_name": "Example Company",
        "job_title": "Junior Developer",
        "location": "Remote",
        "salary_min": 60000,
        "salary_max": 75000,
        "status": status,
        "date_found": "2026-08-04 10:00:00",
        "url": "https://example.com/job",
    }


def read_response_rows(response):
    csv_reader = csv.DictReader(io.StringIO(response.text))
    return list(csv_reader)


def test_export_job_leads_returns_downloadable_csv(monkeypatch):
    received_filter = {}

    def fake_get_all_job_leads(status_filter=None):
        received_filter["status"] = status_filter
        return [make_job_lead("New")]

    monkeypatch.setattr(
        main_module,
        "get_all_job_leads",
        fake_get_all_job_leads,
    )

    client = TestClient(main_module.app)
    response = client.get("/job-leads/export")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert response.headers["content-disposition"] == (
        'attachment; filename="job_leads.csv"'
    )
    assert received_filter["status"] is None

    rows = read_response_rows(response)

    assert len(rows) == 1
    assert rows[0]["Company Name"] == "Example Company"
    assert rows[0]["Status"] == "New"


def test_export_job_leads_forwards_status_filter(monkeypatch):
    received_filter = {}

    def fake_get_all_job_leads(status_filter=None):
        received_filter["status"] = status_filter
        return [make_job_lead("Archived")]

    monkeypatch.setattr(
        main_module,
        "get_all_job_leads",
        fake_get_all_job_leads,
    )

    client = TestClient(main_module.app)
    response = client.get(
        "/job-leads/export",
        params={"status": "Archived"},
    )

    assert response.status_code == 200
    assert received_filter["status"] == "Archived"

    rows = read_response_rows(response)

    assert len(rows) == 1
    assert rows[0]["Status"] == "Archived"
