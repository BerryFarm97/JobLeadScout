import csv
import io

COLUMNS = {
    "company_name": "Company Name",
    "job_title": "Job Title",
    "location": "Location",
    "salary_min": "Salary Minimum",
    "salary_max": "Salary Maximum",
    "status": "Status",
    "date_found": "Date Found",
    "url": "Listing URL",
}


def db_to_csv(csv_dictionaries):
    csv_io = io.StringIO()
    job_leads_writer = csv.DictWriter(csv_io, fieldnames=COLUMNS, extrasaction="ignore")

    job_leads_writer.writerow(COLUMNS)
    job_leads_writer.writerows(csv_dictionaries)

    csv_result_in_memory = csv_io.getvalue()

    return csv_result_in_memory
