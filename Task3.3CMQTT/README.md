# SIT210 Task 3.2C – MQTT Publish and Subscribe

## Project Overview
This project uses an Arduino Nano 33 IoT, an ultrasonic sensor, and two LEDs to demonstrate MQTT publish-subscribe communication.

The ultrasonic sensor is used to detect two gestures:
- Wave
- Pat

When a wave is detected, the Arduino publishes the user's name to the topic `ES/Wave`.  
When a pat is detected, the Arduino publishes the user's name to the topic `ES/Pat`.

The Arduino also subscribes to both topics:
- Messages on `ES/Wave` turn both LEDs ON
- Messages on `ES/Pat` turn both LEDs OFF

## Hardware Used
- Arduino Nano 33 IoT
- HC-SR04 ultrasonic sensor
- 2 LEDs
- 2 resistors
- Breadboard and jumper wires

## MQTT Broker
- Broker: broker.emqx.io
- Port: 1883

## Topics Used
- ES/Wave
- ES/Pat

## Gesture Logic
- Wave: distance between 5 cm and 20 cm
- Pat: distance less than 5 cm

## Modular Programming
The code is divided into separate functions:
- connectWiFi()
- reconnectMQTT()
- getDistance()
- detectGesture()
- callback()

This makes the program easier to understand, test, and maintain.

## Author
Sachkirat Singh
