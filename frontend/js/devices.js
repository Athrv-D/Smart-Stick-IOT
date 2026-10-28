async function loadDevices() {
  const body = document.getElementById("deviceTableBody");

  try {
    const response = await fetch("http://127.0.0.1:8000/devices/");
    const devices = await response.json();

    body.innerHTML = devices
      .map(
        (device) => `
          <tr>
            <td>${device.id}</td>
            <td>${device.name}</td>
            <td>${device.status}</td>
            <td>${device.battery_level}%</td>
            <td>${device.location}</td>
          </tr>
        `
      )
      .join("");
  } catch (error) {
    console.error("Failed to fetch devices", error);
  }
}

loadDevices();
