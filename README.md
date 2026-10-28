# Smart Stick IoT

A single-device Smart Stick monitoring system for caregivers and personal use. The project is designed around a FastAPI backend, PostgreSQL-ready data storage, and a lightweight frontend dashboard for monitoring device health, sensor events, and emergency alerts.

## Overview

This project is intended for a single Smart Stick device, which is suitable for personal use and caregiver monitoring. The backend exposes HTTP endpoints that can be called by an ESP8266-powered device or by a Python simulator until hardware arrives.

## Architecture

- Frontend: HTML, CSS, JavaScript
- Backend: FastAPI
- Database: PostgreSQL (ready for production), SQLite fallback for local testing
- Device communication: HTTP-based API
- Simulated device testing: Python script sends sensor data over HTTP

## Repository structure

```text
smart-stick/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── device.py
│   │   ├── sensor_event.py
│   │   ├── emergency.py
│   │   └── device_settings.py
│   ├── schemas/
│   │   ├── device.py
│   │   ├── sensor.py
│   │   └── emergency.py
│   ├── routers/
│   │   ├── devices.py
│   │   ├── sensor_data.py
│   │   ├── emergencies.py
│   │   └── settings.py
│   └── services/
│       ├── device_service.py
│       ├── sensor_service.py
│       └── notification_service.py
├── frontend/
│   ├── index.html
│   ├── devices.html
│   ├── alerts.html
│   ├── settings.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── dashboard.js
│       ├── devices.js
│       ├── alerts.js
│       └── settings.js
├── simulator/
│   └── device_simulator.py
├── .env.example
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Features

- Device registration and status tracking
- Sensor monitoring with simulated ultrasonic data
- Emergency event storage and alert tracking
- Dashboard for real-time device summary
- Settings configuration for alert thresholds and notification preferences
- Device simulator for testing without hardware

## Local setup

### 1) Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment

Copy the example environment file:

```bash
cp .env.example .env
```

### 4) Start PostgreSQL with Docker

```bash
docker compose up -d
```

### 5) Start the backend

```bash
uvicorn backend.main:app --reload
```

Then open:

- API docs: http://127.0.0.1:8000/docs
- Dashboard: frontend/index.html in the browser

## Device simulator

Run the simulator to generate sensor events and emergency data:

```bash
python simulator/device_simulator.py
```

The simulator posts HTTP payloads to the FastAPI backend in the same way an ESP8266 device would.

## Notes

- This is designed primarily for one Smart Stick device, but the structure can be extended later for multiple devices.
- Until GSM hardware is connected, SMS notification is simulated, not sent through a real SIM800L module.
- The project uses PostgreSQL by default, but it can be run in SQLite mode for easier local testing if needed.
