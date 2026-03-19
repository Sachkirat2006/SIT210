# SIT210 Task 4.1P – Handling Interrupts

## Project Overview
This project implements an interrupt-based smart lighting system using an Arduino Nano 33 IoT.

The system uses a PIR motion sensor to detect Linda’s arrival at the door and a BH1750 light sensor to determine whether it is dark. If motion is detected and the light level is below a threshold, both LEDs turn on automatically. A slider switch is also included as a backup manual interrupt input to turn on the lights if motion detection fails.

## Hardware Used
- Arduino Nano 33 IoT
- PIR motion sensor
- BH1750 light sensor
- Slider switch
- 2 LEDs
- 2 resistors
- Breadboard and jumper wires

## Software Design
The program uses interrupts to detect events from:
- PIR motion sensor
- Slider switch

Interrupt service routines set flags, and the main loop handles:
- light level reading from BH1750
- LED control
- Serial Monitor messages
- automatic turn-off timer

## Features
- Motion-based automatic lighting in dark conditions
- Manual backup lighting using slider switch
- Serial Monitor event logging
- Automatic light timeout after activation

## Files
- Task4.1Interrupts.ino
- README.md
- circuit-diagram.png
- serial-monitor-log.png
- video-link.txt

## Author
Sachkirat Singh
