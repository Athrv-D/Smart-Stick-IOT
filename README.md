# Smart Stick IoT

Built a software system for your Smart Stick IoT project that supports people with multiple disabilities and enables caregivers to real-time monitoring, alert system, automatic emergency calls & SMS.

## Project structure

- `backend/` — FastAPI API and database models
- `frontend/` — UI pages for monitoring and settings
- `simulator/` — sample device simulator for sensor data generation
- `requirements.txt` — Python dependencies
- `.gitignore` — default Git ignores

## Quick start

1. Create a virtual environment
2. Install dependencies
3. Start the API server
4. Open the frontend pages in a browser

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

## API docs

Once the backend is running, open:

- http://127.0.0.1:8000/docs

## Features

- Device registration and monitoring
- Sensor event ingestion
- Emergency alert handling
- Caregiver dashboard UI
- Smart stick settings management

## Default stack

- FastAPI
- SQLAlchemy
- SQLite
- HTML/CSS/JavaScript
- Python simulator
