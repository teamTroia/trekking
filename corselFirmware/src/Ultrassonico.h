#include <defines.h>
#include <Controle.h>
// defines variables
long duration;
int distance;
void initUltrassonico() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}
void distCone() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2;
  // Prints the distance on the Serial Monitor
  Serial.print("Distance: ");
  Serial.println(distance);
  if(distance <= 300){
    FW_PKS.writeMicroseconds(1500);
    ANG_PKS.writeMicroseconds(1500);
    pinMode(LEDCONE,LOW);
    delayMicroseconds(400);
    pinMode(LEDCONE,HIGH);
    delayMicroseconds(400);
  }
}
