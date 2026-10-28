import random
import time

import requests

BASE_URL = "http://127.0.0.1:8000"


def register_device():
    payload = {
        "device_id": "STICK_001",
        "name": "Smart Stick 001",
        "status": "online",
        "connection_type": "wifi",
        "battery_level": 96.5,
        "location": "Home",
        "is_active": True,
    }
    response = requests.post(f"{BASE_URL}/devices/", json=payload)
    print("Device registered:", response.status_code, response.json())


def send_sensor_data():
    payload = {
        "device_id": 1,
        "distance_cm": round(random.uniform(30, 180), 2),
        "status": "obstacle_detected" if random.random() < 0.35 else "clear",
        "event_type": "obstacle_scan",
    }
    response = requests.post(f"{BASE_URL}/sensor/data", json=payload)
    print("Sensor event:", response.status_code, response.json())


def trigger_emergency():
    payload = {
        "device_id": 1,
        "emergency_type": "manual_button",
        "severity": "high",
        "description": "Emergency button pressed by user",
        "notification_status": "pending",
        "resolved": False,
    }
    response = requests.post(f"{BASE_URL}/emergencies/", json=payload)
    print("Emergency event:", response.status_code, response.json())


if __name__ == "__main__":
    register_device()
    while True:
        send_sensor_data()
        if random.random() < 0.08:
            trigger_emergency()
        time.sleep(5)
