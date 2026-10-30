# Smart Stick IoT

A caregiver monitoring application for **one physical Smart Stick** built around an ESP8266 controller.

## What it does

- Monitors one registered stick and its Wi-Fi heartbeat.
- Displays battery level and recent ultrasonic distance readings.
- Stores sensor events and emergency-button events.
- Lets a caregiver review and resolve emergency records.
- Stores obstacle threshold, buzzer, vibration, and notification settings.
- Provides a Python simulator while the physical hardware is being assembled.

## Stack

- Backend: FastAPI + SQLAlchemy
- Local database: SQLite
- Frontend: HTML, CSS, vanilla JavaScript
- Device communication: HTTP over Wi-Fi
- Planned cellular fallback: SIM800L (SMS integration is not yet implemented)

## Project layout

```text
backend/       FastAPI application, models, schemas, routers and services
frontend/      Caregiver dashboard, stick status, alerts and settings
simulator/     Python HTTP simulator for one stick
```

## Local setup (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create your local environment file from the example:

```powershell
Copy-Item .env.example .env
```

4. Start the API from the repository root:

```powershell
uvicorn backend.main:app --reload
```

5. Open the API documentation at http://127.0.0.1:8000/docs. Open `frontend/index.html` in a browser for the caregiver interface.

## Simulator

In a second terminal, activate the same virtual environment and run:

```powershell
python simulator/device_simulator.py
```

The simulator registers or reuses `STICK_001`, uses the database ID returned by the API, and sends sensor readings and occasional emergency events.

## Important implementation boundaries

- The app is intentionally configured for one stick. The database's internal device primary key remains in place to preserve foreign-key relationships.
- Sensor POST requests update the stick's last-seen heartbeat. The dashboard considers the stick online when a heartbeat arrived within the last two minutes.
- Notification delivery currently returns a simulated status. Real SMS delivery requires the SIM800L integration and a tested power supply.
- Local buzzer and vibration alerts must ultimately be implemented on the ESP8266 so they continue working without Wi-Fi, backend, or GSM service.
- SQLite is used by default for local development. Back up `smart_stick.db` before any future database migration.
