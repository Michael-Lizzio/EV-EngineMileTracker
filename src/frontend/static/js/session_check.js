function checkSession() {
    fetch("/auth/check_session")
        .then(response => response.json())
        .then(data => {
            if (data.message === "User not logged in") {
                alert("Session expired. Logging out...");
                window.location.href = "/login";  // Redirect to login page
            }
        })
        .catch(error => console.error("Error checking session:", error));
}

// Run this check every 5 minutes
setInterval(checkSession, 300000);
