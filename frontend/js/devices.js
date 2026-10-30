const API_BASE = "http://127.0.0.1:8000";

function displayDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "—" : date.toLocaleString();
}

async function loadStickStatus() {
  const error = document.getElementById("deviceError");
  try {
    const response = await fetch(`${API_BASE}/dashboard`);
    if (!response.ok) throw new Error("Could not load stick status.");
    const data = await response.json();
    if (!data.device) throw new Error(data.message || "Smart Stick is not registered.");

    const device = data.device;
    const online = device.status === "online";
    const badge = document.getElementById("statusBadge");
    badge.textContent = online ? "Connected" : "Offline";
    badge.className = `status-badge ${online ? "status-online" : "status-offline"}`;
    document.getElementById("stickName").textContent = device.name;
    document.getElementById("stickId").textContent = `Device ID: ${device.device_id}`;
    document.getElementById("connectionType").textContent = device.connection_type || "—";
    document.getElementById("battery").textContent = `${Math.round(device.battery_level ?? 0)}%`;
    document.getElementById("location").textContent = device.location || "Not set";
    document.getElementById("lastSeen").textContent = displayDate(device.last_seen);
    document.getElementById("distance").textContent = data.latest_sensor ? `${data.latest_sensor.distance_cm} cm` : "No reading";
    document.getElementById("sensorStatus").textContent = data.latest_sensor?.status?.replaceAll("_", " ") || "Waiting";

    const history = document.getElementById("sensorHistory");
    history.replaceChildren();
    if (!data.sensor_events?.length) {
      const li = document.createElement("li");
      li.className = "empty-state";
      li.textContent = "No sensor readings received yet.";
      history.appendChild(li);
    } else {
      data.sensor_events.forEach(event => {
        const li = document.createElement("li");
        const strong = document.createElement("strong");
        strong.textContent = `${event.distance_cm} cm · ${event.status.replaceAll("_", " ")}`;
        const span = document.createElement("span");
        span.textContent = `${event.event_type} · ${displayDate(event.timestamp)}`;
        li.append(strong, span);
        history.appendChild(li);
      });
    }
  } catch (err) {
    error.textContent = err.message;
  }
}

loadStickStatus();
setInterval(loadStickStatus, 15000);
