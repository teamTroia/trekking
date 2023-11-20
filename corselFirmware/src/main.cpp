#include <Arduino.h>
// #include <defines.h>
// #include <motor.h>
#include <Serial.h>
// #include <giroscopio.h>
#include <Controle.h>
//#include <Odometria.h>
#include <Ultrassonico.h>

int leitura, eixoX, valEixoX;
void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  initPKS();
  Serial.begin(9600);
  init_mpu();
  initUltrassonico();
}

void loop()
{
  eixoX = SerialConvertion();
  testeMotor(eixoX);
  distCone();
  
  //getpulse(1900,1500);
}