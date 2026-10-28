async function loadDashboard() {
  try {
    const response = await fetch("http://127.0.0.1:8000/devices/");
    const devices = await response.json();

    const total = devices.length;
    const online = devices.filter((device) => device.status === "online").length;
    const offline = total - online;
    const battery = total
      ? Math.round(
          devices.reduce((sum, device) => sum + Number(device.battery_level || 0), 0) / total
        )
      : 0;

    document.getElementById("totalDevices").textContent = total;
    document.getElementById("onlineDevices").textContent = online;
    document.getElementById("offlineDevices").textContent = offline;
    document.getElementById("batteryHealth").textContent = `${battery}%`;

    const eventsList = document.getElementById("recentEvents");
    const alertsList = document.getElementById("recentAlerts");

    eventsList.innerHTML = devices.length
      ? devices
          .slice(0, 4)
          .map(
            (device) =>
              `<li>Device ${device.device_id}: ${device.status} • Battery ${device.battery_level}%</li>`
          )
          .join("")
      : "<li>No recent events.</li>";

    alertsList.innerHTML = "<li>No emergency alerts yet.</li>";
  } catch (error) {
    console.error("Failed to load dashboard data", error);
  }
}

loadDashboard();
