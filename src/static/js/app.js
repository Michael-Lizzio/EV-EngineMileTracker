document.getElementById("tripForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const tripData = {
        date: document.getElementById("date").value,
        odometer_start: parseInt(document.getElementById("odometer_start").value),
        odometer_end: parseInt(document.getElementById("odometer_end").value),
        gallons_used: parseFloat(document.getElementById("gallons_used").value),
        mpg: parseFloat(document.getElementById("mpg").value),
    };

    const response = await fetch("/add_trip", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(tripData),
    });

    const result = await response.json();
    alert(result.message);
});
