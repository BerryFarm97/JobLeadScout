import csv
import io

from app.exporter import COLUMNS, db_to_csv


def parse_csv(csv_text):
    csv_reader = csv.DictReader(io.StringIO(csv_text))
    return csv_reader.fieldnames, list(csv_reader)


def test_db_to_csv_writes_headers_for_empty_list():
    csv_text = db_to_csv([])

    headers, rows = parse_csv(csv_text)

    assert headers == list(COLUMNS.values())
    assert rows == []


def test_db_to_csv_exports_selected_job_lead_fields():
    job_leads = [
        {
            "id": 1,
            "source_job_id": "source-123",
            "job_source": "Adzuna",
            "company_name": "Example Company, Inc.",
            "job_title": "Junior Python Developer",
            "location": "Houston, Texas",
            "salary_min": 60000,
            "salary_max": None,
            "salary_interval": "year",
            "status": "new",
            "date_found": "2026-08-04 10:00:00",
            "url": "https://example.com/job/123",
            "job_description": "An intentionally excluded field.",
        }
    ]

    csv_text = db_to_csv(job_leads)

    headers, rows = parse_csv(csv_text)

    assert headers == list(COLUMNS.values())
    assert rows == [
        {
            "Company Name": "Example Company, Inc.",
            "Job Title": "Junior Python Developer",
            "Location": "Houston, Texas",
            "Salary Minimum": "60000",
            "Salary Maximum": "",
            "Status": "new",
            "Date Found": "2026-08-04 10:00:00",
            "Listing URL": "https://example.com/job/123",
        }
    ]
