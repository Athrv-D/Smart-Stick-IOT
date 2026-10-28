async function loadAlerts() {
  const list = document.getElementById("alertsList");

  try {
    const response = await fetch("http://127.0.0.1:8000/emergencies/");
    const alerts = await response.json();

    if (!alerts.length) {
      list.innerHTML = "<li>No emergency alerts recorded.</li>";
      return;
    }

    list.innerHTML = alerts
      .map(
        (alert) => `
          <li>
            <strong>${alert.emergency_type}</strong> • ${alert.severity} • ${alert.notification_status}
          </li>
        `
      )
      .join("");
  } catch (error) {
    console.error("Failed to fetch alerts", error);
  }
}

loadAlerts();
