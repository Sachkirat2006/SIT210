#include <Wire.h>
#include <BH1750.h>
#include <WiFiNINA.h>

// ===== WiFi Credentials =====
const char* ssid = "iPhone";
const char* password = "Sachkirat";

// ===== IFTTT Webhook =====
const char* host = "maker.ifttt.com";
String key = "buD3WuRjQxCfAPAIRHtGm67pjZ9X--NbqTUYux4NVdO";  // paste your key here

// ===== Sensor =====
BH1750 lightMeter;

// ===== Trigger Settings =====
float threshold = 1500.0;   // adjust if needed
bool sunlightPresent = false;

// ===== WiFi Client =====
WiFiClient client;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  lightMeter.begin();

  connectWiFi();
}

void loop() {
  float lux = lightMeter.readLightLevel();

  Serial.print("Light: ");
  Serial.println(lux);

  // ===== Sunlight START =====
  if (lux > threshold && sunlightPresent == false) {
    Serial.println("Sunlight detected!");
    sendIFTTT("sunlight_started");
    sunlightPresent = true;
  }

  // ===== Sunlight STOP =====
  if (lux <= threshold && sunlightPresent == true) {
    Serial.println("Sunlight stopped!");
    sendIFTTT("sunlight_stopped");
    sunlightPresent = false;
  }

  delay(5000);  // check every 5 seconds
}

// ===== Connect WiFi =====
void connectWiFi() {
  Serial.print("Connecting to WiFi...");

  while (WiFi.begin(ssid, password) != WL_CONNECTED) {
    Serial.print(".");
    delay(2000);
  }

  Serial.println("\nConnected!");
}

// ===== Send IFTTT Notification =====
void sendIFTTT(String event) {
  if (client.connect(host, 80)) {
    String url = "/trigger/" + event + "/with/key/" + key;

    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n\r\n");

    Serial.println("Notification sent: " + event);
  } else {
    Serial.println("Connection to IFTTT failed");
  }
}
