# Smart Stick IoT

A caregiver monitoring application for **one physical Smart Stick** built around an ESP8266 controller.

## Capabilities
- Single-device caregiver dashboard and SQLite storage.
- ESP8266 HTTP API for sensor readings and independent heartbeat.
- Obstacle distance and water sensor readings with caregiver-configurable thresholds.
- Caregiver settings synchronization for buzzer and vibration.
- Emergency event records and device-reported SMS delivery status.
- Python simulator for backend testing before hardware is assembled.
- Arduino IDE firmware starter in `firmware/`.

## Stack
FastAPI, SQLAlchemy, SQLite, HTML/CSS/vanilla JS, ESP8266 Arduino core, HTTP over Wi-Fi, optional SIM800L SMS.

## Local backend setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
Open http://127.0.0.1:8000/docs. Keep the existing `smart_stick.db`; startup applies additive SQLite columns for water readings/settings. Back it up before upgrades.

## Simulator
```powershell
python simulator/device_simulator.py
```
The simulator registers/reuses `STICK_001`, sends sensor events and heartbeat, and occasionally creates a simulated emergency.

## ESP8266
See [firmware setup and wiring cautions](firmware/README.md). Set `API_BASE` to the PC's LAN IP (not localhost), and use the same Wi-Fi network. Do not connect 5V sensor outputs directly to ESP8266 GPIO.

## API contract
- `POST /devices/` register/reuse the configured stick.
- `POST /devices/heartbeat` update last-seen and connection/battery data.
- `GET /settings/` retrieve obstacle/water thresholds and local alert toggles.
- `PUT /settings/` update caregiver settings.
- `POST /sensor/data` submit distance/water readings using stable `device_code`.
- `POST /emergencies/` record an emergency using stable `device_code`.
- `POST /emergencies/{id}/delivery` report SMS result as `sent` or `failed`.

Legacy simulator payloads with numeric `device_id` remain accepted for sensor and emergency records.

## Important status
- Local buzzer/vibration behavior is in the ESP8266 firmware and must be validated on the bench.
- SMS sending is not active yet. The firmware scaffold leaves SIM800L disabled until its exact board, supply, antenna, serial pins, SIM/operator 2G support and recipient number are confirmed. After sending SMS, firmware should POST delivery status.
- The prototype is not a certified mobility aid. Do not rely on it as the user's only navigation or emergency system.
