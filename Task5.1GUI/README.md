# SIT210 Task 5.1P – Making a Graphical User Interface

## Overview
This project uses a Raspberry Pi, Python, Tkinter, and 3 LEDs to create a simple GUI for controlling room lights.

The three LEDs represent:
- Living Room
- Bathroom
- Closet

The GUI includes:
- 3 radio buttons
- 1 exit button

When a radio button is selected, the corresponding LED turns ON and the other two LEDs turn OFF.

## Hardware
- Raspberry Pi
- Breadboard
- 3 LEDs
- Resistors
- Jumper wires

## Software
- Python 3
- Tkinter
- RPi.GPIO

## GPIO Pins
- Living Room LED → GPIO 17
- Bathroom LED → GPIO 27
- Closet LED → GPIO 22

## Functionality
- Living Room selected → only living room LED ON
- Bathroom selected → only bathroom LED ON
- Closet selected → only closet LED ON
- Exit button closes GUI and cleans up GPIO

## Author
Sachkirat Singh
