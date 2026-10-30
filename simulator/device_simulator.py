import random
import time

import requests

BASE_URL = "http://127.0.0.1:8000"
DEVICE_ID = "STICK_001"
device_pk = None


def register_device():
    global device_pk
    payload = {
        "device_id": DEVICE_ID,
        "name": "Smart Stick 001",
        "status": "online",
        "connection_type": "wifi",
        "battery_level": 96.5,
        "location": "Home",
        "is_active": True,
    }
    response = requests.post(f"{BASE_URL}/devices/", json=payload, timeout=10)
    response.raise_for_status()
    device_pk = response.json()["id"]
    print(f"Connected simulator to {DEVICE_ID} (database id: {device_pk})")


def send_sensor_data():
    payload = {
        "device_id": device_pk,
        "distance_cm": round(random.uniform(30, 180), 2),
        "status": "obstacle_detected" if random.random() < 0.35 else "clear",
        "event_type": "obstacle_scan",
        "battery_level": round(random.uniform(75, 100), 1),
    }
    response = requests.post(f"{BASE_URL}/sensor/data", json=payload, timeout=10)
    response.raise_for_status()
    print("Sensor event:", response.json())


def trigger_emergency():
    payload = {
        "device_id": device_pk,
        "emergency_type": "manual_button",
        "severity": "high",
        "description": "Emergency button pressed by user",
    }
    response = requests.post(f"{BASE_URL}/emergencies/", json=payload, timeout=10)
    response.raise_for_status()
    print("Emergency event:", response.json())


if __name__ == "__main__":
    register_device()
    while True:
        send_sensor_data()
        if random.random() < 0.08:
            trigger_emergency()
        time.sleep(5)
