const API_BASE = "http://127.0.0.1:8000";

function formatDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "—" : date.toLocaleString();
}

function addListItem(list, title, detail, className = "") {
  const item = document.createElement("li");
  if (className) item.className = className;
  const strong = document.createElement("strong");
  strong.textContent = title;
  const small = document.createElement("span");
  small.textContent = detail;
  item.append(strong, small);
  list.appendChild(item);
}

async function loadDashboard() {
  const error = document.getElementById("dashboardError");
  try {
    const response = await fetch(`${API_BASE}/dashboard`);
    if (!response.ok) throw new Error("Could not load dashboard data.");
    const data = await response.json();

    const device = data.device;
    const badge = document.getElementById("connectionBadge");
    const events = document.getElementById("recentEvents");
    const alerts = document.getElementById("recentAlerts");
    events.replaceChildren();
    alerts.replaceChildren();

    if (!device) {
      badge.textContent = "Not registered";
      badge.className = "status-badge status-offline";
      document.getElementById("deviceName").textContent = "Smart Stick not registered";
      document.getElementById("deviceMeta").textContent = data.message || "Register your stick to begin.";
      ["connectionValue", "batteryValue", "distanceValue"].forEach(id => {
        document.getElementById(id).textContent = "—";
      });
      addListItem(events, "No sensor data", "Waiting for the stick to be registered.", "empty-state");
      addListItem(alerts, "No emergency data", "No events available yet.", "empty-state");
      return;
    }

    const online = device.status === "online";
    badge.textContent = online ? "Connected" : "Offline";
    badge.className = `status-badge ${online ? "status-online" : "status-offline"}`;
    document.getElementById("deviceName").textContent = device.name;
    document.getElementById("deviceMeta").textContent = `Device ID: ${device.device_id} · ${device.location || "Location not set"}`;
    document.getElementById("lastSeen").textContent = `Last communication: ${formatDate(device.last_seen)}`;
    document.getElementById("connectionValue").textContent = online ? "Online" : "Offline";
    document.getElementById("connectionHint").textContent = device.connection_type || "Unknown connection";
    document.getElementById("batteryValue").textContent = `${Math.round(device.battery_level ?? 0)}%`;

    const sensor = data.latest_sensor;
    document.getElementById("distanceValue").textContent = sensor ? `${sensor.distance_cm} cm` : "—";
    document.getElementById("obstacleHint").textContent = sensor ? sensor.status.replaceAll("_", " ") : "No sensor reading yet";

    const unresolved = (data.emergencies || []).filter(item => !item.resolved).length;
    document.getElementById("openAlertsValue").textContent = unresolved;

    if (data.sensor_events?.length) {
      data.sensor_events.forEach(event => addListItem(events, `${event.distance_cm} cm · ${event.status.replaceAll("_", " ")}`, `${event.event_type} · ${formatDate(event.timestamp)}`));
    } else {
      addListItem(events, "No readings recorded", "Sensor activity will appear here.", "empty-state");
    }

    if (data.emergencies?.length) {
      data.emergencies.forEach(item => addListItem(alerts, `${item.emergency_type} · ${item.severity}`, `${item.resolved ? "Resolved" : "Needs attention"} · ${formatDate(item.created_at)}`));
    } else {
      addListItem(alerts, "No emergency alerts", "No emergency events have been recorded.", "empty-state");
    }
  } catch (err) {
    error.textContent = `${err.message} Check that the FastAPI server is running.`;
    console.error(err);
  }
}

loadDashboard();
setInterval(loadDashboard, 15000);
