import random
import time

import requests

BASE_URL = "http://127.0.0.1:8000"


def register_device():
    payload = {
        "name": "Smart Stick Device 01",
        "device_id": "ST-001",
        "status": "online",
        "battery_level": 96.5,
        "location": "Warehouse A",
        "is_active": True,
    }
    response = requests.post(f"{BASE_URL}/devices/", json=payload)
    print("Device registered:", response.status_code, response.json())


def send_sensor_data():
    payload = {
        "device_id": 1,
        "temperature": round(random.uniform(24, 40), 2),
        "vibration": round(random.uniform(5, 20), 2),
        "pressure": round(random.uniform(10, 30), 2),
        "moisture": round(random.uniform(30, 80), 2),
    }
    response = requests.post(f"{BASE_URL}/sensor/data", json=payload)
    print("Sensor data:", response.status_code, response.json())


if __name__ == "__main__":
    register_device()
    while True:
        send_sensor_data()
        time.sleep(5)
