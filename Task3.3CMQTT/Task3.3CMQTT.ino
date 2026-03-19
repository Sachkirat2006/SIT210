#include <WiFiNINA.h>
#include <PubSubClient.h>

// ===== WiFi =====
const char* ssid = "iPhone";
const char* password = "Sachkirat";

// ===== MQTT =====
const char* mqtt_server = "broker.emqx.io";
WiFiClient wifiClient;
PubSubClient client(wifiClient);

// ===== Pins =====
const int trigPin = 2;
const int echoPin = 3;

const int led1 = 6;
const int led2 = 7;

// ===== Variables =====
long duration;
float distance;
String lastGesture = "";

// ===== Setup =====
void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);

  connectWiFi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

// ===== Loop =====
void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();

  distance = getDistance();

  Serial.print("Distance: ");
  Serial.println(distance);

  detectGesture();

  delay(1000);
}

// ===== Distance Function =====
float getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  float dist = duration * 0.034 / 2;

  return dist;
}

// ===== Gesture Detection =====
void detectGesture() {
  if (distance > 5 && distance < 15 && lastGesture != "wave") {
    Serial.println("Wave detected!");
    client.publish("ES/Wave", "Sachkirat");
    lastGesture = "wave";
  }

  else if (distance < 5 && lastGesture != "pat") {
    Serial.println("Pat detected!");
    client.publish("ES/Pat", "Sachkirat");
    lastGesture = "pat";
  }
}

// ===== MQTT Callback =====
void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";

  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Message arrived on ");
  Serial.print(topic);
  Serial.print(": ");
  Serial.println(message);

  if (String(topic) == "ES/Wave") {
    digitalWrite(led1, HIGH);
    digitalWrite(led2, HIGH);
  }

  if (String(topic) == "ES/Pat") {
    digitalWrite(led1, LOW);
    digitalWrite(led2, LOW);
  }
}

// ===== WiFi =====
void connectWiFi() {
  Serial.print("Connecting to WiFi...");

  while (WiFi.begin(ssid, password) != WL_CONNECTED) {
    Serial.print(".");
    delay(2000);
  }

  Serial.println("\nConnected!");
}

// ===== MQTT Reconnect =====
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");

    if (client.connect("Sachkirat_Client")) {
      Serial.println("Connected!");

      client.subscribe("ES/Wave");
      client.subscribe("ES/Pat");

    } else {
      Serial.print("Failed, retrying...");
      delay(2000);
    }
  }
}
