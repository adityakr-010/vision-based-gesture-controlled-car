#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>
#include <AsyncUDP.h>

// pins
#define ENA 13
#define IN1 12
#define IN2 14
#define IN3 27
#define IN4 26
#define ENB 25

// WiFi
const char *ssid = "gesture";
const char *password = "hello123";

AsyncUDP udp;
unsigned int udpPort = 8888;

void setup() {
  Serial.begin(115200);
  delay(1000);  // Give serial monitor time to connect

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);
  stopMotors();

  WiFi.mode(WIFI_AP);
  
  WiFi.softAP(ssid, password, 6, 0, 4);  // Channel 6, not hidden, max 4 connections
  WiFi.setTxPower(WIFI_POWER_19_5dBm);   // Max transmit power

  Serial.println();
  Serial.println("AP Configuration:");
  Serial.print("SSID: ");
  Serial.println(ssid);
  Serial.print("Password: ");
  Serial.println(password);
  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP());

  // UDP server
  if(udp.listen(udpPort)) {
    Serial.print("UDP Listening on port ");
    Serial.println(udpPort);
    
    udp.onPacket([](AsyncUDPPacket packet) {
      String command = String((char*)packet.data());
      command.trim();
      Serial.print("Received command: ");
      Serial.println(command);
      
      if(command == "FORWARD") moveForward();
      else if(command == "BACKWARD") moveBackward();
      else if(command == "LEFT") turnLeft();
      else if(command == "RIGHT") turnRight();
      else stopMotors();
    });
  } else {
    Serial.println("Failed to start UDP server!");
  }
}

void loop() {
}

// Motor control
void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void moveForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 200);  // Adjust PWM value for speed (0-255)
  analogWrite(ENB, 200);
}

void moveBackward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 200);
  analogWrite(ENB, 200);
}

void turnLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);  
  digitalWrite(IN3, HIGH);  
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 200);
  analogWrite(ENB, 200);
}

void turnRight() {
  digitalWrite(IN1, HIGH); 
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);   
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 200);
  analogWrite(ENB, 200);
}
