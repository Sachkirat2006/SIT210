# SIT210 Task 5.2C – Change the Light Intensity Using GUI

## Student Details
- Name: Sachkirat Singh
- Unit: SIT210 Embedded Systems Development

## Project Overview
This project extends Task 5.1P by adding PWM-based light intensity control for the living room LED using a GUI on Raspberry Pi.

The system includes:
- Living Room LED with adjustable brightness using a slider
- Bathroom LED with ON/OFF control
- Closet LED with ON/OFF control

The GUI was developed using Python and Tkinter.

## Hardware Used
- Raspberry Pi
- Breadboard
- 3 LEDs
- Resistors
- Jumper wires

## GPIO Pins
- Living Room LED → GPIO 18 (PWM)
- Bathroom LED → GPIO 27
- Closet LED → GPIO 22

## GUI Features
- Radio button for Living Room
- Radio button for Bathroom
- Radio button for Closet
- Slider to control living room brightness
- Exit button

## How the system works
- When Living Room is selected, the slider changes the PWM duty cycle and adjusts LED brightness.
- When Bathroom is selected, only the bathroom LED turns ON.
- When Closet is selected, only the closet LED turns ON.
- The Exit button closes the GUI and safely cleans up GPIO.

## Concepts Used
- Python Tkinter GUI
- Raspberry Pi GPIO
- PWM (Pulse Width Modulation)
- Duty cycle control
- Event-driven programming

## Files
- `gui.py` → main Python GUI code
- `README.md` → project description
- `screenshots/` → GUI and hardware images

## Author
Sachkirat Singh
