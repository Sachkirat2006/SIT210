#include <SPI.h>
#include <WiFiNINA.h>
#include <PubSubClient.h>

const char* ssid = "iPhone";
const char* password = "Sachkirat";

const char* mqtt_server = "172.20.10.2";

WiFiClient wifiClient;
PubSubClient client(wifiClient);

const int switchPin = 2;
const int ledPin = 6;
const int buzzerPin = 7;

bool reminderActive = false;
unsigned long reminderStartTime = 0;
const unsigned long responseTime = 15000;

String backupPatient = "";
String backupDose = "";
String backupTime = "";
bool backupUsed = false;

void setup() {
  Serial.begin(9600);
  delay(3000);

  pinMode(switchPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  digitalWrite(ledPin, LOW);
  noTone(buzzerPin);

  Serial.println("Medication Reminder System Starting...");

  connectWiFi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();

  checkBackupSchedule();

  if (reminderActive) {
    checkUserResponse();
    checkMissedDose();
  }
}

void connectWiFi() {
  Serial.print("Connecting to WiFi");

  while (WiFi.begin(ssid, password) != WL_CONNECTED) {
    delay(2000);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
}

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");

    if (client.connect("MedicineArduino001")) {
      Serial.println("connected");
      client.subscribe("medicine/command");
      Serial.println("Subscribed to medicine/command");
    } else {
      Serial.print("failed, rc=");
      Serial.println(client.state());
      delay(2000);
      break;
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";

  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Message: ");
  Serial.println(message);

  if (message.startsWith("take_medicine")) {
    startReminder();
  }

  if (message.startsWith("backup_schedule|")) {
    saveBackupSchedule(message);
  }
}

void saveBackupSchedule(String message) {
  int first = message.indexOf('|');
  int second = message.indexOf('|', first + 1);
  int third = message.indexOf('|', second + 1);

  backupPatient = message.substring(first + 1, second);
  backupDose = message.substring(second + 1, third);
  backupTime = message.substring(third + 1);
  backupUsed = false;

  Serial.println("Backup schedule stored on Arduino:");
  Serial.println(backupPatient);
  Serial.println(backupDose);
  Serial.println(backupTime);
}

void checkBackupSchedule() {
  if (backupTime == "" || backupUsed == true || reminderActive == true) {
    return;
  }

  unsigned long epochTime = WiFi.getTime();

  if (epochTime == 0) {
    return;
  }

  int currentHour = (epochTime % 86400L) / 3600;
  int currentMinute = (epochTime % 3600) / 60;

  String currentTime = "";

  if (currentHour < 10) currentTime += "0";
  currentTime += String(currentHour);
  currentTime += ":";

  if (currentMinute < 10) currentTime += "0";
  currentTime += String(currentMinute);

  if (currentTime == backupTime && !client.connected()) {
    Serial.println("MQTT disconnected. Backup alarm triggered by Arduino.");
    startReminder();
    backupUsed = true;
  }
}

void startReminder() {
  reminderActive = true;
  reminderStartTime = millis();

  digitalWrite(ledPin, HIGH);
  tone(buzzerPin, 1000);

  Serial.println("Medicine reminder started");
}

void checkUserResponse() {
  if (digitalRead(switchPin) == LOW) {
    reminderActive = false;

    digitalWrite(ledPin, LOW);
    noTone(buzzerPin);

    Serial.println("Dose taken");
    client.publish("medicine/status", "taken");

    delay(500);
  }
}

void checkMissedDose() {
  if (millis() - reminderStartTime >= responseTime) {
    reminderActive = false;

    digitalWrite(ledPin, LOW);
    noTone(buzzerPin);

    Serial.println("Dose missed");
    client.publish("medicine/status", "missed");
  }
}
