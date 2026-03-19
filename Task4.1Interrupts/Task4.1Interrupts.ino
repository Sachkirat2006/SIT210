#include <Wire.h>
#include <BH1750.h>

// ===== Pins =====
const int pirPin = 2;
const int switchPin = 3;
const int led1 = 6;
const int led2 = 7;

// ===== Sensor =====
BH1750 lightMeter;

// ===== Interrupt flags =====
volatile bool motionTriggered = false;
volatile bool switchTriggered = false;

// ===== Settings =====
float darkThreshold = 100.0;                  // adjust after testing
const unsigned long lightOnDuration = 10000; // 10 seconds
unsigned long lightsOnTime = 0;
bool lightsAreOn = false;

// ===== Optional debounce / cooldown =====
volatile unsigned long lastSwitchInterrupt = 0;
volatile unsigned long lastMotionInterrupt = 0;
const unsigned long switchDebounceMs = 300;
const unsigned long motionCooldownMs = 1000;

void setup() {
  delay(2000);
  Serial.begin(9600);
  delay(1000);

  Serial.println("System ready");

  pinMode(pirPin, INPUT);
  pinMode(switchPin, INPUT_PULLUP);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);

  turnLightsOff();

  Wire.begin();
  if (lightMeter.begin()) {
    Serial.println("BH1750 started");
  } else {
    Serial.println("BH1750 failed to start");
  }

  attachInterrupt(digitalPinToInterrupt(pirPin), motionISR, RISING);
  attachInterrupt(digitalPinToInterrupt(switchPin), switchISR, FALLING);

  Serial.println("Interrupts attached");
  Serial.println("Wait about 30 to 60 seconds for PIR warm-up.");
}

void loop() {
  // ===== Handle motion interrupt =====
  if (motionTriggered) {
    motionTriggered = false;

    // Ignore repeated triggers while lights are already ON
    if (!lightsAreOn) {
      float lux = lightMeter.readLightLevel();

      Serial.print("Motion interrupt detected. Light level: ");
      Serial.print(lux);
      Serial.println(" lx");

      if (lux < darkThreshold) {
        turnLightsOn();
        Serial.println("It is dark. PIR interrupt turned LED1 and LED2 ON.");
      } else {
        Serial.println("Motion detected, but it is not dark. Lights remain OFF.");
      }
    }
  }

  // ===== Handle switch interrupt =====
  if (switchTriggered) {
    switchTriggered = false;

    turnLightsOn();
    Serial.println("Backup slider switch interrupt triggered. LED1 and LED2 turned ON.");
  }

  // ===== Auto turn OFF after a while =====
  if (lightsAreOn && millis() - lightsOnTime >= lightOnDuration) {
    turnLightsOff();
    Serial.println("Light timer expired. LED1 and LED2 turned OFF.");
  }

  delay(50);
}

void turnLightsOn() {
  digitalWrite(led1, HIGH);
  digitalWrite(led2, HIGH);
  lightsAreOn = true;
  lightsOnTime = millis();
}

void turnLightsOff() {
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  lightsAreOn = false;
}

// ===== Interrupt Service Routines =====
void motionISR() {
  unsigned long currentTime = millis();

  if (currentTime - lastMotionInterrupt > motionCooldownMs) {
    motionTriggered = true;
    lastMotionInterrupt = currentTime;
  }
}

void switchISR() {
  unsigned long currentTime = millis();

  if (currentTime - lastSwitchInterrupt > switchDebounceMs) {
    switchTriggered = true;
    lastSwitchInterrupt = currentTime;
  }
}
