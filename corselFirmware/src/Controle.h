#include <defines.h>
#include <motor.h>

int ang, frente;
void testeMotor(int eixoX)
{
    if (eixoX != 0)
    {
        if (eixoX > 0 && eixoX < 220)
        {
            frente = 1340;
            ang = 1156;
        }
        else if (eixoX > 420)
        
        {
            frente = 1760;
            ang = 1894;
        }
        else if (eixoX >= 220 && eixoX <= 420)
        {
            frente = 1876;
            ang = 1500;
        }
    }

    FW_PKS.writeMicroseconds(frente);
    ANG_PKS.writeMicroseconds(ang);
    delay(400);
}

float PID(float target, float atual)
{
    float kp = 60;

    float error = target - atual;
    float output = error * kp;
    return output;
}

float pidCamera(int target, int atual)
{
    int kp = 0.00035;

    int error = target - atual;
    int output = error * kp;
    return output;
}

void align(int eixoX){
    float gyro = readAngularSpeed();
}

void getpulse(int frente, int ang){
    FW_PKS.writeMicroseconds(frente);
    ANG_PKS.writeMicroseconds(ang);
    
}