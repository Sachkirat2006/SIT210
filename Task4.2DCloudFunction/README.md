# SIT210 Task 4.2D – Calling a Function from the Web

## Student Details
- Name: Sachkirat Singh
- Unit: SIT210 Embedded Systems Development

---

## Project Overview
This project demonstrates a cloud-connected lighting control system using an Arduino Nano 33 IoT, Arduino Cloud, and a web-based frontend interface.

The system allows a carer to remotely control lights in three rooms:
- Living Room
- Bathroom
- Closet

Each room is represented by an LED.

---

## System Architecture

The system follows a three-layer architecture:

Frontend (HTML Page)  
→ Backend (Arduino Cloud)  
→ Device (Arduino Nano 33 IoT)

User actions trigger cloud variable updates, which call a function on the Arduino to control LEDs.

---

## Hardware Components

- Arduino Nano 33 IoT
- Breadboard
- 3 LEDs
- Resistors
- Jumper wires

---

## Software Components

- Arduino Cloud (backend communication)
- HTML page (frontend interface)
- Arduino C++ code (device logic)

---

## Key Features

- Web-triggered function using Arduino Cloud
- controlLight(String room) function implementation
- Real-time LED control via cloud variables
- State tracking for each room light
- Modular and event-driven code design

---

## HTML Interface

The HTML page provides:
- ON/OFF controls for each room
- Display of current light state
- User-friendly interface for carers

---

## Screenshots

### HTML Page
![HTML Page](screenshots/html-page.png)

### Arduino Cloud Dashboard
![Dashboard](screenshots/dashboard.png)

### Serial Monitor Output
![Serial](screenshots/serial-monitor.png)

### Circuit Setup
![Circuit](screenshots/circuit.jpg)

---

## Block Diagram

![Block Diagram](diagrams/block-diagram.png)

---

## How It Works

1. User interacts with web interface or cloud dashboard
2. Cloud variable is updated
3. Arduino receives update
4. controlLight(String room) function is executed
5. Corresponding LED is turned ON/OFF

---

## Improvements

- Full REST API integration between HTML and Arduino Cloud
- Real-time state synchronisation with frontend
- User authentication for secure access
- Mobile app integration
- Data logging for usage tracking

---

## GitHub Repository Structure
