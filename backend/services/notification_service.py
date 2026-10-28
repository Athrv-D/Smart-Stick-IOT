def send_alert(emergency_type: str, message: str):
    print(f"[ALERT] {emergency_type}: {message}")
    return {"status": "simulated", "message": message}
