const jobForm = document.getElementById("job-search-form");

function refreshJobLeads(event) {
    event.preventDefault();

    const formData = new FormData(jobForm);
    const location = formData.get("location");
    const keywords = formData.get("keywords");

    const locationParam = new URLSearchParams(location);
    const keywordParam = new URLSearchParams(keywords);

    console.log(locationParam.toString(), keywordParam.toString());
}

jobForm.addEventListener("submit", refreshJobLeads);