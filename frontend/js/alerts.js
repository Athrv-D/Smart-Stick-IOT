async function loadAlerts() {
  const alertsList = document.getElementById("alertsList");

  try {
    const response = await fetch("http://127.0.0.1:8000/emergencies/");
    const alerts = await response.json();

    if (!alerts.length) {
      alertsList.innerHTML = "<li>No alerts</li>";
      return;
    }

    alertsList.innerHTML = alerts
      .map(
        (alert) => `
          <li>
            <strong>${alert.type}</strong> - ${alert.severity} - ${alert.status}
          </li>
        `
      )
      .join("");
  } catch (error) {
    console.error("Failed to fetch alerts", error);
  }
}

loadAlerts();
