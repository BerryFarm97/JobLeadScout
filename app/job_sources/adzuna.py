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
