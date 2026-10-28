async function loadDevices() {
  const tableBody = document.querySelector("#deviceTable tbody");

  try {
    const response = await fetch("http://127.0.0.1:8000/devices/");
    const devices = await response.json();

    tableBody.innerHTML = devices
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
