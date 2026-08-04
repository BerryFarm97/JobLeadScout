const jobForm = document.getElementById("job-search-form");
const refreshButton = document.getElementById("refresh-button");
const statusDropdowns = document.querySelectorAll(".status-select");
const deleteButtons = document.querySelectorAll(".delete-lead-button");

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

statusDropdowns.forEach(function (statusDropdown) {
    statusDropdown.addEventListener("change", async function (event) {
        const newStatus = event.target.value;
        const jobLeadId = event.target.dataset.jobLeadId;

        const urlParams = new URLSearchParams();
        urlParams.set("new_status", newStatus);

        const queryStatusString = urlParams.toString();
        const statusUpdateUrl = `/job-leads/${jobLeadId}/status?${queryStatusString}`;

        try {
            const statusResponse = await fetch(statusUpdateUrl, {
                method: "PATCH",
            });

            const apiStatusResponse = await statusResponse.json()

            if (statusResponse.ok) {
                window.location.reload();
            } else {
                window.alert(apiStatusResponse.detail);
            }
        } catch (error) {
            console.error(error);
            window.alert("Unable to complete request. Please try again later.");
        }
    });
});

deleteButtons.forEach(function (deleteButton) {
    deleteButton.addEventListener("click", async function (event) {
        const jobId = event.currentTarget.dataset.jobLeadId;
        const deleteUrl = `/job-leads/${jobId}`;

        const userChoice = window.confirm("Are you sure you want to permanently delete? This cannot be undone.");
        if (!userChoice) {
            return;
        }
        deleteButton.disabled = true;
        try {
            const deleteResponse = await fetch(deleteUrl, {
                method: "DELETE",
            });

            const apiDeleteResponse = await deleteResponse.json();

            if (deleteResponse.ok) {
                window.location.reload();
            } else {
                window.alert(apiDeleteResponse.detail);
            }
        } catch (error) {
            console.error(error);
            window.alert("Unable to delete job lead. Please try again later");
        } finally {
            deleteButton.disabled = false;
        }
    });
});

jobForm.addEventListener("submit", refreshJobLeads);