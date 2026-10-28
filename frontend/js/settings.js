document.getElementById("settingsForm").addEventListener("submit", async (event) => {
  event.preventDefault();

  const form = event.target;
  const payload = {
    obstacle_threshold: Number(form.obstacle_threshold.value),
    buzzer_enabled: form.buzzer_enabled.checked,
    vibration_enabled: form.vibration_enabled.checked,
    emergency_contact_number: form.emergency_contact_number.value,
    notification_preferences: form.notification_preferences.value,
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/settings/1", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();
    console.log("Settings saved:", result);
    alert("Settings saved successfully.");
  } catch (error) {
    console.error("Failed to save settings", error);
  }
});
