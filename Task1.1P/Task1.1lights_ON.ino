// ===== Pin Definitions =====
const int buttonPin = 2;
const int porchLight = LED_BUILTIN;
const int hallwayLight = 6;

// ===== Timing =====
const int porchTime = 30000;    // 30 seconds
const int hallwayTime = 60000;  // 60 seconds

// ===== Setup =====
void setup()
{
  pinMode(buttonPin, INPUT);
  pinMode(porchLight, OUTPUT);
  pinMode(hallwayLight, OUTPUT);

  Serial.begin(9600);
}

// ===== Main Loop =====
void loop()
{
  if (buttonPressed())
  {
    activateLights();
  }
}

// ===== Function: Check Button =====
bool buttonPressed()
{
  if (digitalRead(buttonPin) == HIGH)
  {
    delay(50); // debounce
    return true;
  }
  return false;
}

// ===== Function: Activate Lights =====
void activateLights()
{
  // Turn BOTH lights ON
  digitalWrite(porchLight, HIGH);
  digitalWrite(hallwayLight, HIGH);

  // Wait 30 seconds
  delay(porchTime);

  // Turn OFF porch light
  digitalWrite(porchLight, LOW);

  // Wait remaining 30 seconds
  delay(hallwayTime - porchTime);

  // Turn OFF hallway light
  digitalWrite(hallwayLight, LOW);
}