# SIT210 Task 3.1P – Trigger and Notification Based on Sensor Data

## Project Overview
This project uses an Arduino Nano 33 IoT and a BH1750 light sensor to monitor sunlight exposure for Linda’s terrarium.

When sunlight starts hitting the terrarium, the system sends a notification through IFTTT. When sunlight stops, the system sends another notification. The solution uses WiFi to connect the Arduino to the internet and IFTTT webhooks to trigger the alerts.

## Hardware Used
- Arduino Nano 33 IoT
- BH1750 light sensor
- Breadboard and jumper wires

## Software and Services Used
- Arduino IDE
- BH1750 library
- WiFiNINA library
- IFTTT Webhooks
- IFTTT Notifications / Email

## System Behaviour
- Reads light intensity in lux from the BH1750 sensor
- Compares the lux value with a threshold
- Detects when sunlight starts
- Detects when sunlight stops
- Sends notifications using IFTTT

## Modular Programming
The code is divided into separate parts for:
- connecting to WiFi
- reading the light level
- checking the trigger condition
- sending IFTTT notifications

This makes the program easier to understand and maintain.

## Files
- Task3.1Trigger.ino
- README.md
- block-diagram.png
- trigger-code.png
- notification-code.png

## Author
Sachkirat Singh
