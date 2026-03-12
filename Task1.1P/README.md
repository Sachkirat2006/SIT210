# SIT210 Task 1.1P – Switching ON Lights

## Project Overview
This project implements a simple smart assisted living lighting system using an Arduino Nano 33 IoT.

The system is designed for Linda’s home. When Linda activates a slider switch, both the porch light and hallway light turn on together to improve visibility and safety when entering the house at night.

The porch light remains on for 30 seconds while the hallway light remains on for 60 seconds.

## Hardware Components
- Arduino Nano 33 IoT
- Built-in LED (Porch Light)
- External LED (Hallway Light)
- Slider switch
- Breadboard
- Jumper wires
- 220Ω resistor
- 10kΩ resistor

## System Behaviour
1. Slider switch is activated
2. Both LEDs turn ON together
3. Built-in LED turns OFF after 30 seconds
4. External LED turns OFF after 60 seconds

## Modular Programming
The program is divided into multiple functions to improve readability and maintainability.

- `buttonPressed()` detects when the slider switch is triggered
- `activateLights()` controls the timing of the lighting system
- `setup()` initializes pins and serial communication
- `loop()` continuously monitors the switch state

This modular structure makes the program easier to debug, modify, and extend in future smart home applications.

## Repository Structure
Task1.1P/
- Task1.1Lights_ON.ino
- README.md
- circuit-schematic.png

## Demonstration Video
Video link: Add your YouTube or Panopto link here

## Author
Sachkirat Singh
SIT210 – Embedded Systems Development
