#ifndef MOTOR_H
#define MOTOR_H

#include <defines.h>
#include <giroscopio.h>
#include <servo.h>
Servo FW_PKS, ANG_PKS;

void initPKS() {
        FW_PKS.attach(fw_pks);
        ANG_PKS.attach(ang_pks);
}

void stopPKS() {
    FW_PKS.writeMicroseconds(1500);
    ANG_PKS.writeMicroseconds(1500);
}

void motorsControl() {
    if (Serial.available()){
        if(Serial.read() == 'Direita'){
            FW_PKS.writeMicroseconds(2000);
            ANG_PKS.writeMicroseconds(1800);
        }
        if(Serial.read() == 'Esquerda'){
            FW_PKS.writeMicroseconds(2000);
            ANG_PKS.writeMicroseconds(1200);
        }
        else{
            FW_PKS.writeMicroseconds(1500);
            ANG_PKS.writeMicroseconds(1500);
        }
    }
}

#endif