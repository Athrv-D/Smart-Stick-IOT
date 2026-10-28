async function loadDashboard() {
  try {
    const response = await fetch("http://127.0.0.1:8000/devices/");
    const devices = await response.json();

    const online = devices.filter((device) => device.status === "online").length;
    const battery = devices.length
      ? Math.round(
          devices.reduce((sum, device) => sum + device.battery_level, 0) / devices.length
        )
      : 0;

    document.getElementById("onlineDevices").textContent = online;
    document.getElementById("openAlerts").textContent = "0";
    document.getElementById("batteryHealth").textContent = `${battery}%`;
  } catch (error) {
    console.error("Dashboard fetch failed:", error);
  }
}

loadDashboard();
