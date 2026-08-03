const jobForm = document.getElementById("job-search-form");
const refreshButton = document.getElementById("refresh-button");

async function refreshJobLeads(event) {
    event.preventDefault();

    const formData = new FormData(jobForm);
    const location = formData.get("location");
    const keywords = formData.get("keywords");

    const searchParams = new URLSearchParams();

    searchParams.set("keywords", keywords);
    searchParams.set("location", location);

    const queryString = searchParams.toString();
    const refreshUrl = `/job-leads/refresh?${queryString}`;

    refreshButton.disabled = true;
    refreshButton.textContent = "Refreshing...";

    try {
        const response = await fetch(refreshUrl, {
            method: "POST",
        });

        const jobResponse = await response.json();

        if (response.ok) {
            window.location.reload();
        } else {
            window.alert(jobResponse.detail);
        }
    } catch (error) {
        console.error(error);
        window.alert("Unable to complete request. Please try again later.");
    } finally {
        refreshButton.disabled = false;
        refreshButton.textContent = "Refresh Jobs";
    }
}

jobForm.addEventListener("submit", refreshJobLeads);