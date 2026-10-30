const API_BASE = "http://127.0.0.1:8000";

function alertDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "—" : date.toLocaleString();
}

async function resolveAlert(id) {
  const response = await fetch(`${API_BASE}/emergencies/${id}`, { method: "PATCH" });
  if (!response.ok) throw new Error("Could not resolve this emergency.");
  await loadAlerts();
}

async function loadAlerts() {
  const list = document.getElementById("alertsList");
  const error = document.getElementById("alertsError");
  error.textContent = "";
  try {
    const response = await fetch(`${API_BASE}/emergencies/`);
    if (!response.ok) throw new Error("Could not fetch emergency history.");
    const items = await response.json();
    list.replaceChildren();

    if (!items.length) {
      const empty = document.createElement("li");
      empty.className = "empty-state";
      empty.textContent = "No emergency alerts recorded.";
      list.appendChild(empty);
      return;
    }

    items.forEach(item => {
      const li = document.createElement("li");
      li.className = "alert-item";
      const content = document.createElement("div");
      const title = document.createElement("strong");
      title.textContent = `${item.emergency_type} · ${item.severity}`;
      const details = document.createElement("span");
      details.textContent = `${item.description || "No additional details"} · ${alertDate(item.created_at)}`;
      const status = document.createElement("span");
      status.className = "muted";
      status.textContent = `Notification: ${item.notification_status} · ${item.resolved ? "Resolved" : "Open"}`;
      content.append(title, details, status);
      li.appendChild(content);

      if (!item.resolved) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "button-secondary";
        button.textContent = "Mark resolved";
        button.addEventListener("click", async () => {
          button.disabled = true;
          try { await resolveAlert(item.id); }
          catch (err) { error.textContent = err.message; button.disabled = false; }
        });
        li.appendChild(button);
      }
      list.appendChild(li);
    });
  } catch (err) {
    error.textContent = err.message;
  }
}

document.getElementById("refreshAlerts").addEventListener("click", loadAlerts);
loadAlerts();
