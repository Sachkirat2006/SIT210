#include <WiFiNINA.h>
#include <ThingSpeak.h>
#include "DHT.h"

// ===== WiFi =====
const char* ssid = "iPhone";
const char* password = "Sachkirat";

// ===== ThingSpeak =====
unsigned long channelNumber = 3305473;
const char* writeAPIKey = "O36I8HVPU10DBEWB";

// ===== Sensors =====
#define DHTPIN 3
#define DHTTYPE DHT11
const int lightPin = A0;

WiFiClient client;
DHT dht(DHTPIN, DHTTYPE);

// ===== Setup =====
void setup() {
  Serial.begin(9600);
  delay(2000);

  dht.begin();
  connectWiFi();
  ThingSpeak.begin(client);
}

// ===== Loop =====
void loop() {
  float temperature = readTemperature();
  int lightValue = readLight();

  sendToThingSpeak(temperature, lightValue);

  delay(30000);
}

// ===== Functions =====

void connectWiFi() {
  Serial.print("Connecting to WiFi");

  while (WiFi.begin(ssid, password) != WL_CONNECTED) {
    Serial.print(".");
    delay(5000);
  }

  Serial.println("\nConnected!");
}

float readTemperature() {
  float temp = dht.readTemperature();

  if (isnan(temp)) {
    Serial.println("Temp error");
    return 0;
  }

  Serial.print("Temp: ");
  Serial.println(temp);

  return temp;
}

int readLight() {
  int light = analogRead(lightPin);

  Serial.print("Light: ");
  Serial.println(light);

  return light;
}

void sendToThingSpeak(float temp, int light) {
  ThingSpeak.setField(1, temp);
  ThingSpeak.setField(2, light);

  int result = ThingSpeak.writeFields(channelNumber, writeAPIKey);

  if (result == 200) {
    Serial.println("Upload success");
  } else {
    Serial.print("Error: ");
    Serial.println(result);
  }
}
