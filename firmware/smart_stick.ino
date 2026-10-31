/*
  Smart Stick ESP8266 firmware - integration baseline
  Board: NodeMCU ESP-12E (ESP8266)
  Libraries: ESP8266 board package, ArduinoJson 7.x, ESP8266 core HTTPClient/WiFi.

  IMPORTANT HARDWARE SAFETY:
  - HC-SR04 Echo is 5V: use a resistor voltage divider before ESP8266 GPIO.
  - Never power SIM800L from the ESP8266 3.3V pin. Use a separate regulated supply
    appropriate for your exact SIM800L board (typically ~4.0V, capable of ~2A peaks),
    and connect grounds together.
  - Drive the vibration motor through a transistor/MOSFET + flyback diode, not GPIO.
  - Verify your board's pin labels and boot-strap behavior before wiring.
  - A0 input range differs by NodeMCU board; verify the board's divider/range.
  - Local buzzer/vibration alerts run independently of Wi-Fi and GSM.

  Set credentials and confirm pins before powering hardware.
*/
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>
#include <SoftwareSerial.h>

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* API_BASE = "http://192.168.1.10:8000"; // PC LAN IP, not 127.0.0.1
const char* DEVICE_CODE = "STICK_001";
const char* FIRMWARE_VERSION = "0.1.0";

// Review and adapt these pins to the exact NodeMCU board and wiring.
const uint8_t PIN_TRIG = D1;
const uint8_t PIN_ECHO = D2;       // HC-SR04 Echo MUST be level-shifted to 3.3V
const uint8_t PIN_BUZZER = D5;
const uint8_t PIN_VIBRATION = D6;  // transistor/MOSFET driver input
const uint8_t PIN_EMERGENCY = D7;  // button to GND, INPUT_PULLUP
const uint8_t PIN_WATER = A0;

// SIM800L serial is optional until supply and pins have been validated.
// SoftwareSerial(rx, tx). These pins are only a suggested starting point;
// check boot-strap pins and your exact board before enabling.
#define ENABLE_SIM800L 0
#if ENABLE_SIM800L
SoftwareSerial gsm(D0, D8);
#endif

float obstacleThresholdCm = 80.0;
int waterThreshold = 500;
bool buzzerEnabled = true;
bool vibrationEnabled = true;
unsigned long lastHeartbeat = 0;
unsigned long lastSensorPost = 0;
unsigned long lastSettingsFetch = 0;
unsigned long lastButtonEvent = 0;

WiFiClient wifiClient;

void localAlert(bool active) {
  digitalWrite(PIN_BUZZER, active && buzzerEnabled ? HIGH : LOW);
  digitalWrite(PIN_VIBRATION, active && vibrationEnabled ? HIGH : LOW);
}

float readDistanceCm() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(3);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  unsigned long duration = pulseIn(PIN_ECHO, HIGH, 30000UL);
  if (duration == 0) return -1.0;
  return duration * 0.0343f / 2.0f;
}

bool postJson(const String& path, JsonDocument& doc, String* responseBody = nullptr) {
  if (WiFi.status() != WL_CONNECTED) return false;
  HTTPClient http;
  String url = String(API_BASE) + path;
  if (!http.begin(wifiClient, url)) return false;
  http.addHeader("Content-Type", "application/json");
  String body;
  serializeJson(doc, body);
  int code = http.POST(body);
  Serial.print("POST ");
  Serial.print(path);
  Serial.print(" | HTTP status: ");
  Serial.println(code);

  if (code > 0) {
    String response = http.getString();
    Serial.print("Response: ");
    Serial.println(response);
    if (responseBody) *responseBody = response;
  } else {
    Serial.print("HTTP error: ");
    Serial.println(http.errorToString(code));
  }

  http.end();
  return code >= 200 && code < 300;
}

void sendHeartbeat() {
  if (WiFi.status() != WL_CONNECTED) return;
  JsonDocument doc;
  doc["device_code"] = DEVICE_CODE;
  doc["connection_type"] = "wifi";
  doc["firmware_version"] = FIRMWARE_VERSION;
  // Add calibrated battery percentage here only after measuring your battery circuit.
  postJson("/devices/heartbeat", doc);
}

void fetchSettings() {
  if (WiFi.status() != WL_CONNECTED) return;
  HTTPClient http;
  if (!http.begin(wifiClient, String(API_BASE) + "/settings/")) return;
  int code = http.GET();
  Serial.print("GET /settings/ | HTTP status: ");
  Serial.println(code);
  if (code > 0) {
    Serial.print("Settings response: ");
    Serial.println(http.getString());
  } else {
    Serial.print("Settings request error: ");
    Serial.println(http.errorToString(code));
  }

  // Fetch the response again for JSON parsing.
  if (code == 200) {
    String settingsResponse = http.getString();
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, settingsResponse);
    if (!error) {
      obstacleThresholdCm = doc["obstacle_threshold"] | obstacleThresholdCm;
      waterThreshold = doc["water_threshold"] | waterThreshold;
      buzzerEnabled = doc["buzzer_enabled"] | buzzerEnabled;
      vibrationEnabled = doc["vibration_enabled"] | vibrationEnabled;
    }
  }
  http.end();
}

void postSensorReading(float distance, int waterRaw, bool waterDetected, bool obstacleDetected) {
  JsonDocument doc;
  doc["device_code"] = DEVICE_CODE;
  doc["distance_cm"] = distance < 0 ? 0 : distance;
  doc["water_detected"] = waterDetected;
  doc["water_value"] = waterRaw;
  doc["status"] = waterDetected ? "water_detected" :
                  obstacleDetected ? "obstacle_detected" : "clear";
  doc["event_type"] = "sensor_scan";
  postJson("/sensor/data", doc);
}

#if ENABLE_SIM800L
bool waitForGsm(const char* expected, unsigned long timeoutMs) {
  String received;
  unsigned long started = millis();
  while (millis() - started < timeoutMs) {
    while (gsm.available()) {
      char c = static_cast<char>(gsm.read());
      received += c;
      if (received.indexOf(expected) >= 0) return true;
    }
    delay(10);
  }
  return false;
}

bool sendSms(const String& phone, const String& message) {
  if (phone.length() < 8) return false;
  while (gsm.available()) gsm.read();
  gsm.println("AT");
  if (!waitForGsm("OK", 2000)) return false;
  gsm.println("AT+CMGF=1");
  if (!waitForGsm("OK", 2000)) return false;
  gsm.print("AT+CMGS=\"");
  gsm.print(phone);
  gsm.println("\"");
  if (!waitForGsm(">", 5000)) return false;
  gsm.print(message);
  gsm.write(26); // Ctrl+Z submits the SMS
  return waitForGsm("+CMGS:", 20000) && waitForGsm("OK", 5000);
}

void reportSmsDelivery(int emergencyId, bool sent) {
  if (emergencyId <= 0 || WiFi.status() != WL_CONNECTED) return;
  JsonDocument statusDoc;
  statusDoc["status"] = sent ? "sent" : "failed";
  postJson(String("/emergencies/") + emergencyId + "/delivery", statusDoc);
}
#endif

void sendEmergency(const char* type, const char* description) {
  JsonDocument doc;
  doc["device_code"] = DEVICE_CODE;
  doc["emergency_type"] = type;
  doc["severity"] = "high";
  doc["description"] = description;
  String response;
  if (!postJson("/emergencies/", doc, &response)) return;

#if ENABLE_SIM800L
  JsonDocument result;
  if (deserializeJson(result, response) != DeserializationError::Ok) return;
  int emergencyId = result["id"] | 0;

  // Retrieve the caregiver's configured number; never hard-code a recipient.
  HTTPClient settingsHttp;
  if (!settingsHttp.begin(wifiClient, String(API_BASE) + "/settings/")) {
    reportSmsDelivery(emergencyId, false);
    return;
  }
  int settingsCode = settingsHttp.GET();
  String phone;
  if (settingsCode == 200) {
    JsonDocument settingsDoc;
    if (deserializeJson(settingsDoc, settingsHttp.getString()) == DeserializationError::Ok) {
      phone = settingsDoc["emergency_contact_number"] | "";
    }
  }
  settingsHttp.end();

  String smsText = String("SMART STICK EMERGENCY: ") + type + ". " + description;
  bool sent = settingsCode == 200 && sendSms(phone, smsText);
  reportSmsDelivery(emergencyId, sent);
#endif
}

void setup() {
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_VIBRATION, OUTPUT);
  pinMode(PIN_EMERGENCY, INPUT_PULLUP);
  localAlert(false);
  Serial.begin(115200);
#if ENABLE_SIM800L
  gsm.begin(9600);
#endif
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.println();
  Serial.println("Connecting to Wi-Fi...");
  const unsigned long wifiStart = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - wifiStart < 20000UL) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.println("Wi-Fi connected!");
    Serial.print("ESP8266 IP: ");
    Serial.println(WiFi.localIP());
    Serial.print("Backend: ");
    Serial.println(API_BASE);
  } else {
    Serial.println();
    Serial.println("Wi-Fi connection failed. Local alerts remain active.");
    Serial.print("Wi-Fi status code: ");
    Serial.println(WiFi.status());
  }
}

void loop() {
  const unsigned long now = millis();
  const bool wifiConnected = WiFi.status() == WL_CONNECTED;

  // Local sensing and warning logic is intentionally independent of network state.
  float distance = readDistanceCm();
  int waterRaw = analogRead(PIN_WATER);
  bool waterDetected = waterRaw < waterThreshold; // Calibrate dry/wet values for your sensor.
  bool obstacleDetected = distance > 0 && distance <= obstacleThresholdCm;
  localAlert(waterDetected || obstacleDetected);

  if (wifiConnected && now - lastSensorPost >= 5000UL) {
    postSensorReading(distance, waterRaw, waterDetected, obstacleDetected);
    lastSensorPost = now;
  }
  if (wifiConnected && now - lastHeartbeat >= 30000UL) {
    sendHeartbeat();
    lastHeartbeat = now;
  }
  if (wifiConnected && now - lastSettingsFetch >= 60000UL) {
    fetchSettings();
    lastSettingsFetch = now;
  }
  if (digitalRead(PIN_EMERGENCY) == LOW && now - lastButtonEvent > 1500UL) {
    localAlert(true);
    sendEmergency("manual_button", "Emergency button pressed");
    lastButtonEvent = now;
  }
  delay(80);
}
