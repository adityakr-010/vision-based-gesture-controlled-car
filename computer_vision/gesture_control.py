import cv2
import mediapipe as mp
import numpy as np
import socket
import time
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,  
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

ESP_IP = "192.168.4.1"  
ESP_PORT = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cap = cv2.VideoCapture(0)

prev_command = "STOP"
command_sent_time = 0
command_delay = 0.2  

def calculate_finger_status(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_extended = thumb_tip.x < thumb_ip.x
    
    fingers = []
    for tip, pip in [(mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP),
                     (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
                     (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
                     (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP)]:
        tip_pos = hand_landmarks.landmark[tip]
        pip_pos = hand_landmarks.landmark[pip]
        fingers.append(tip_pos.y < pip_pos.y)  
    
    return thumb_extended, fingers

def determine_command(thumb_extended, fingers):
    # Command logic 
    index, middle, ring, pinky = fingers
    # Stop (closed fist)
    if not any([thumb_extended, index, middle, ring, pinky]):
        return "STOP"
    # Forward (index and middle extended)
    if index and middle and not (ring or pinky):
        return "FORWARD"
    # Backward (all fingers extended)
    if all([index, middle, ring, pinky]):
        return "BACKWARD"
    
    if thumb_extended and index and not (middle or ring or pinky):
        return "LEFT"
    
    if thumb_extended and pinky and not (index or middle or ring):
        return "RIGHT"
    
    return "STOP"
  
def send_command(command):
    global prev_command, command_sent_time
    current_time = time.time()
  
    if command != prev_command or (current_time - command_sent_time) > command_delay:
        try:
            sock.sendto(command.encode(), (ESP_IP, ESP_PORT))
            print(f"Sent command: {command}")
            prev_command = command
            command_sent_time = current_time
        except Exception as e:
            print(f"Error sending command: {e}")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    command = "STOP"  # Default 
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            thumb_extended, fingers = calculate_finger_status(hand_landmarks)
            
            # Determine command 
            command = determine_command(thumb_extended, fingers)
    
    # Display command on screen
    cv2.putText(image, f"Command: {command}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    send_command(command)
    
    cv2.imshow('Gesture Controlled Car', image)
    
    # Exit on 'q' key press
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()
sock.close()
