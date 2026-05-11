# Gesture Controlled Car using MediaPipe + ESP32

## Overview

This project implements a **hand gesture controlled robotic car** using:

* **Python + OpenCV + MediaPipe** for hand gesture recognition
* **ESP32** for wireless motor control
* **UDP communication over WiFi**
* **L298N Motor Driver** for driving DC motors

The webcam captures hand gestures, identifies finger positions using MediaPipe, and sends movement commands wirelessly to the ESP32. The ESP32 then controls the motors accordingly.

---

# Features

* Real-time hand tracking
* Wireless control using WiFi + UDP
* Gesture-based movement
* Low latency communication
* Supports:

  * Forward
  * Backward
  * Left
  * Right
  * Stop

---

# Technologies Used

## Python 

* Python
* OpenCV
* MediaPipe
* NumPy
* Socket Programming

## Hardware 

* ESP32
* L298N Motor Driver
* DC Motors
* Robot Chassis
* Battery Pack

---

# Hand Gestures

| Gesture               | Action   |
| --------------------- | -------- |
| Closed Fist           | STOP     |
| Index + Middle Finger | FORWARD  |
| All Fingers Open      | BACKWARD |
| Thumb + Index         | LEFT     |
| Thumb + Pinky         | RIGHT    |

---

# System Architecture

```text
Webcam → MediaPipe Hand Tracking → Gesture Detection
       → UDP Command Transmission → ESP32
       → Motor Driver → Robot Movement
```

---

# Hardware Requirements

| Component          | Quantity  |
| ------------------ | --------- |
| ESP32              | 1         |
| L298N Motor Driver | 1         |
| DC Motors          | 2         |
| Robot Chassis      | 1         |
| Wheels             | 2         |
| Battery Pack       | 1         |
| Jumper Wires       | As needed |
| Laptop with Webcam | 1         |

---

# ESP32 Pin Connections

| ESP32 Pin | L298N Pin |
| --------- | --------- |
| 13        | ENA       |
| 12        | IN1       |
| 14        | IN2       |
| 27        | IN3       |
| 26        | IN4       |
| 25        | ENB       |

---

# Software Installation

## Install Python Dependencies

```bash
pip install opencv-python mediapipe numpy
```

---

# Upload ESP32 Code

1. Open Arduino IDE
2. Install ESP32 board package
3. Select ESP32 board
4. Install required library:

   * AsyncUDP
5. Upload the ESP32 code

---

# WiFi Configuration

Inside ESP32 code:

```cpp
const char *ssid = "realme5G";
const char *password = "hello123";
```

The ESP32 creates its own WiFi Access Point.

---

# Python Configuration

Update ESP32 IP in Python code:

```python
ESP_IP = "192.168.4.1"
ESP_PORT = 8888
```

---

# Running the Project

## Step 1

Power the ESP32 and connect motors.

## Step 2

Connect laptop to ESP32 WiFi network.

## Step 3

Run Python script:

```bash
python gesture_control.py
```

## Step 4

Show gestures in front of webcam.

---

# How It Works

## 1. Hand Detection

MediaPipe detects hand landmarks from webcam frames.

## 2. Finger State Analysis

The system checks whether fingers are extended or folded.

## 3. Gesture Classification

Finger combinations are mapped to commands.

## 4. Wireless Communication

Commands are sent using UDP packets.

## 5. Motor Control

ESP32 receives commands and drives motors accordingly.

---

# Example Commands Sent

```text
FORWARD
BACKWARD
LEFT
RIGHT
STOP
```

---

# Motor Functions

| Function       | Description        |
| -------------- | ------------------ |
| moveForward()  | Moves car forward  |
| moveBackward() | Moves car backward |
| turnLeft()     | Rotates left       |
| turnRight()    | Rotates right      |
| stopMotors()   | Stops all motors   |

---

# Future Improvements

* Add speed control using gestures
* Use two-hand gestures
* Add obstacle avoidance
* Deploy using Raspberry Pi
* Add camera streaming
* Replace UDP with WebSockets/MQTT
* Add mobile app control

---

# Author

Aditya Kumar

---

# License

This project is for educational and learning purposes.
