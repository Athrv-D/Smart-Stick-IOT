document.getElementById("settingsForm").addEventListener("submit", async (event) => {
  event.preventDefault();

  const form = event.target;
  const payload = {
    threshold_temperature: Number(form.threshold_temperature.value),
    threshold_vibration: Number(form.threshold_vibration.value),
    threshold_pressure: Number(form.threshold_pressure.value),
    alert_mode: "sms",
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
    alert("Settings updated successfully");
  } catch (error) {
    console.error("Failed to save settings", error);
  }
});
