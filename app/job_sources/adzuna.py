import httpx


def normalize_adzuna_job(job_data):
    normalized_job_lead = {
        "source_job_id": job_data["id"],
        "job_source": "Adzuna",
        "company_name": job_data["company"]["display_name"],
        "job_title": job_data["title"],
        "url": job_data["redirect_url"],
        "location": job_data["location"]["display_name"],
    }
    return normalized_job_lead


def fetch_adzuna_jobs(app_id, app_key, keywords, location, results_per_page):
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": keywords,
        "where": location,
        "results_per_page": results_per_page,
        "content-type": "application/json",
    }

    response = httpx.get(
        "https://api.adzuna.com/v1/api/jobs/us/search/1", params=params, timeout=10.0
    )
    response.raise_for_status()

    response_data = response.json()
    return response_data["results"]
