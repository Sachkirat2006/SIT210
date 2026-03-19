# SIT210 Task 2.1P – Sending Temperature and Light Data to the Web

## Project Overview
This project uses an Arduino Nano 33 IoT to collect temperature and light data and send the readings to ThingSpeak every 30 seconds.

The system is designed for Linda’s smart assisted living environment so that room conditions can be monitored through a web-based dashboard.

## Hardware Used
- Arduino Nano 33 IoT
- DHT sensor
- Light sensor
- Breadboard
- Jumper wires
- Resistor(s)

## Software and Services Used
- Arduino IDE
- DHT sensor library
- WiFiNINA library
- ThingSpeak library
- ThingSpeak platform

## System Behaviour
- Reads temperature from the DHT sensor
- Reads light level from the light sensor
- Connects to WiFi
- Sends both values to ThingSpeak every 30 seconds

## Modular Programming
The code uses modular programming by separating major tasks into different functions:
- `connectWiFi()`
- `readTemperature()`
- `readLight()`
- `sendToThingSpeak()`

This makes the program easier to read, test, and maintain.

## Files
- `Task2.1WebHook.ino`
- `README.md`
- `circuit-image.png`
- `thingspeak-channel.png`
- `thingspeak-graph-5min.png`

## Author
Sachkirat Singh
