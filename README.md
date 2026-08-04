# Job Lead Scout

Job Lead Scout is a FastAPI web application that retrieves job listings from Adzuna using user-provided keywords and locations. It normalizes and stores the results in SQLite, prevents duplicate listings, and displays job leads through a paginated web dashboard.

Users can organize leads by status, export all or filtered results to CSV, archive leads, and permanently delete archived records. The project builds on the manual workflow of my earlier Job Tracker project by automating job-lead discovery.

## MVP Features

- ☑ Retrieve job listings from the Adzuna API
- ☑ Store essential job-lead information in SQLite
- ☑ Prevent duplicate listings from being saved
- ☑ Search using user-provided keywords and locations
- ☑ Display leads through a paginated web dashboard
- ☑ Filter leads by status
- ☑ Update leads as new, saved, applied, or archived
- ☑ Export all or status-filtered leads to CSV
- ☑ Permanently delete archived leads with confirmation
- ☑ Protect active leads from permanent deletion

## Technology

- Python 3.13+
- FastAPI
- SQLite
- Jinja2
- HTML and CSS
- JavaScript
- HTTPX
- pytest
- uv

## Requirements

Before running the application, you will need:

- Python 3.13 or newer
- The uv package manager
- An Adzuna developer account with an application ID and API key

## Setup

Clone the repository:

```bash
git clone https://github.com/BerryFarm97/JobLeadScout.git
cd JobLeadScout
```

Install the project dependencies:

```bash
uv sync
```

Copy `.env.example` to a new file named `.env`, then add your Adzuna credentials:

```env
ADZUNA_APP_ID=your_application_id
ADZUNA_APP_KEY=your_api_key
```

The `.env` file and local SQLite databases are excluded from version control.

## Running the Application

Start the development server:

```bash
uv run fastapi dev
```

Open the dashboard at:

```text
http://127.0.0.1:8000
```

FastAPI’s interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The SQLite database and required table are created automatically when the application starts.

## Using Job Lead Scout

1. Enter job-search keywords and a location.
2. Select **Refresh Jobs** to retrieve current listings from Adzuna.
3. Review the imported leads on the dashboard.
4. Change a lead’s status to new, saved, applied, or archived.
5. Filter the dashboard using the status tabs.
6. Export all visible categories or the currently filtered status to CSV.
7. Permanently delete an archived lead using its trash button.

Archived leads must be deleted intentionally through a confirmation prompt. The API also prevents non-archived leads from being permanently deleted.

## API Endpoints

| Method   | Endpoint                          | Purpose                                      |
| -------- | --------------------------------- | -------------------------------------------- |
| `GET`    | `/`                               | Display the web dashboard                    |
| `GET`    | `/health`                         | Check application health                     |
| `GET`    | `/job-leads`                      | Return all stored job leads                  |
| `POST`   | `/job-leads/refresh`              | Retrieve and import listings from Adzuna     |
| `PATCH`  | `/job-leads/{job_lead_id}/status` | Update a lead’s status                       |
| `DELETE` | `/job-leads/{job_lead_id}`        | Permanently delete an archived lead          |
| `GET`    | `/job-leads/export`               | Download all or status-filtered leads as CSV |

## Testing

Run the complete automated test suite:

```bash
uv run pytest -v
```

The current suite contains 40 tests covering database operations, Adzuna normalization and importing, API behavior, pagination, status updates, CSV generation, filtered exports, dashboard totals, and protected deletion.

## Possible Future Enhancements

- ☐ Classify listings as remote, local, hybrid, outside the preferred area, or unknown
- ☐ Add explainable match estimates using a user-defined skills profile
- ☐ Add configurable search preferences
- ☐ Deploy the application with persistent database storage
