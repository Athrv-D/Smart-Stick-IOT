const API_BASE = "http://127.0.0.1:8000";
const form = document.getElementById("settingsForm");
const message = document.getElementById("settingsMessage");

async function loadSettings() {
  try {
    const response = await fetch(`${API_BASE}/settings/`);
    if (!response.ok) throw new Error("Could not load settings. Register the stick first.");
    const settings = await response.json();
    form.obstacle_threshold.value = settings.obstacle_threshold ?? 80;
    form.buzzer_enabled.checked = settings.buzzer_enabled ?? true;
    form.vibration_enabled.checked = settings.vibration_enabled ?? true;
    form.emergency_contact_number.value = settings.emergency_contact_number || "";
    form.notification_preferences.value = settings.notification_preferences || "sms";
  } catch (err) {
    message.textContent = err.message;
    message.className = "form-message error-message";
  }
}

form.addEventListener("submit", async event => {
  event.preventDefault();
  message.textContent = "Saving…";
  message.className = "form-message";
  const payload = {
    obstacle_threshold: Number(form.obstacle_threshold.value),
    buzzer_enabled: form.buzzer_enabled.checked,
    vibration_enabled: form.vibration_enabled.checked,
    emergency_contact_number: form.emergency_contact_number.value.trim(),
    notification_preferences: form.notification_preferences.value,
  };

  try {
    const response = await fetch(`${API_BASE}/settings/`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || "Could not save settings.");
    message.textContent = "Settings saved.";
    message.className = "form-message success-message";
  } catch (err) {
    message.textContent = err.message;
    message.className = "form-message error-message";
  }
});

loadSettings();
