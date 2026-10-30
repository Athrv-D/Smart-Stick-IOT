# ESP8266 firmware integration

Open `smart_stick.ino` in Arduino IDE. Select **NodeMCU 1.0 (ESP-12E Module)**.

## Arduino IDE setup
1. Install the ESP8266 board package using the Boards Manager URL from the official ESP8266 Arduino core documentation.
2. Install **ArduinoJson 7.x** from Library Manager.
3. Select the NodeMCU 1.0 board and the correct COM port.
4. Set Wi-Fi credentials.
5. Set `API_BASE` to the computer's LAN IPv4 address, for example `http://192.168.1.10:8000`. The ESP8266 cannot use the PC's `127.0.0.1`.
6. Make sure the PC firewall allows the API port on the trusted private network.
7. Register the device once using the API/simulator, then upload the sketch.

## API contract used by firmware

- `POST /devices/heartbeat`: `device_code`, `connection_type`, optional `battery_level`, optional `firmware_version`.
- `GET /settings/`: obstacle threshold, water threshold, buzzer and vibration enable flags.
- `POST /sensor/data`: stable `device_code`, `distance_cm`, `water_detected`, `water_value`, `status`, `event_type`.
- `POST /emergencies/`: stable `device_code`, `emergency_type`, `severity`, `description`.
- `POST /emergencies/{id}/delivery`: device reports `sent` or `failed` SMS delivery status.

## Pin and electrical checklist

The sketch pin map is a starting point, not a substitute for checking the exact board and module. Confirm pin labels, boot behavior and voltage levels before wiring.

- HC-SR04 Echo is 5V logic: use a resistor divider/level shifter to protect ESP8266 GPIO.
- Water sensor analog output goes to A0 only after checking your NodeMCU board's A0 input range.
- Drive the vibration motor using a transistor/MOSFET driver and flyback diode.
- Use a suitable buzzer driver if its current exceeds GPIO limits.
- SIM800L requires a separate regulated supply capable of high burst current (often around 2A peak); common ground with ESP8266. Do not use the ESP8266 3.3V output.
- SIM800L code is deliberately disabled by default. Validate exact SIM800L board, power, antenna, SIM/operator 2G support, and serial pin selection before enabling it.
- Battery percentage is not sent by the sketch until a voltage-divider/ADC measurement has been calibrated for the actual battery and board.

## SMS behavior

The backend stores the emergency event and returns its database ID. SMS is intended to be sent by SIM800L firmware, then confirmed to the backend using the delivery endpoint. This starter sketch does **not** yet send SMS: recipient-number retrieval and SIM800L electrical/pin validation must be completed before enabling SMS. This prevents sending to a hard-coded or unverified number.

## Local safety behavior

Obstacle/water sensing and buzzer/vibration logic execute on the ESP8266 even when Wi-Fi is disconnected. HTTP reporting and heartbeat are best-effort network functions and do not gate local alerts.

## Calibration before use

Calibrate the water sensor's dry and wet raw ADC readings; confirm whether lower or higher raw values mean water for your exact sensor. Set the dashboard threshold accordingly. Validate obstacle threshold and ultrasonic range with real objects. This is a prototype baseline, not a certified mobility aid; do not rely on it as the user's only means of navigation or emergency communication.
