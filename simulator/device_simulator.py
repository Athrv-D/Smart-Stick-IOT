import random
import time

import requests

BASE_URL = "http://127.0.0.1:8000"
DEVICE_CODE = "STICK_001"


def register_device():
    payload = {
        "device_id": DEVICE_CODE,
        "name": "Smart Stick 001",
        "status": "online",
        "connection_type": "wifi",
        "battery_level": 96.5,
        "location": "Unknown",
        "is_active": True,
    }
    response = requests.post(f"{BASE_URL}/devices/", json=payload, timeout=10)
    response.raise_for_status()
    print(f"Registered simulator for {DEVICE_CODE}")


def send_heartbeat():
    response = requests.post(
        f"{BASE_URL}/devices/heartbeat",
        json={"device_code": DEVICE_CODE, "connection_type": "wifi", "battery_level": 96.5},
        timeout=10,
    )
    response.raise_for_status()


def send_sensor_data():
    distance = round(random.uniform(20, 180), 2)
    water_value = random.randint(100, 900)
    water_detected = water_value < 350
    status = "water_detected" if water_detected else (
        "obstacle_detected" if distance < 80 else "clear"
    )
    payload = {
        "device_code": DEVICE_CODE,
        "distance_cm": distance,
        "water_detected": water_detected,
        "water_value": water_value,
        "status": status,
        "event_type": "sensor_scan",
        "battery_level": round(random.uniform(75, 100), 1),
    }
    response = requests.post(f"{BASE_URL}/sensor/data", json=payload, timeout=10)
    response.raise_for_status()
    print("Sensor event:", response.json())


def trigger_emergency():
    payload = {
        "device_code": DEVICE_CODE,
        "emergency_type": "manual_button",
        "severity": "high",
        "description": "Emergency button pressed by user (simulator)",
    }
    response = requests.post(f"{BASE_URL}/emergencies/", json=payload, timeout=10)
    response.raise_for_status()
    print("Emergency event:", response.json())


if __name__ == "__main__":
    register_device()
    last_heartbeat = 0
    while True:
        send_sensor_data()
        if time.monotonic() - last_heartbeat >= 30:
            send_heartbeat()
            last_heartbeat = time.monotonic()
        if random.random() < 0.08:
            trigger_emergency()
        time.sleep(5)
