def send_alert(message: str):
    print(f"[ALERT] {message}")
    return {"status": "sent", "message": message}
