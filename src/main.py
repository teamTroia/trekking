import numpy as np
import random as rng
import RPi.GPIO as GPIO
import time
import cv2
from control import enableMotors
from visao import procuraCONE

MARGEM_ERRO_CENTRO = 40

# desliga o LED
def offLED(pino):
    time.sleep(1)
    GPIO.output(pino, GPIO.LOW)

# se cone na esquerda
def coneESQ():
    print('O cone esta na esquerda')
    enableMotors(100, -0.15)

# se cone na direita
def coneDIR():
    print('O cone esta na direita')
    enableMotors(100, 0.15)

# se cone em frente
def coneFRE():
    print('O cone esta em frente')
    enableMotors(100, 0)

# liga os LED
def ligaLED(eixoX):
    GPIO.output(eixoX, GPIO.HIGH)
    offLED(eixoX)

# define onde o cone está
def coneCaminho(eixoX):
    if eixoX > 320 + MARGEM_ERRO_CENTRO:
        coneDIR()
    elif eixoX < 320 - MARGEM_ERRO_CENTRO:
        coneESQ()
    else:
        coneFRE()
        
    
    print(eixoX)

def main():
    cap = cv2.VideoCapture(0)
    lastCone = None
    while(1):
        cones = procuraCONE(cap)
        
        if (len(cones) == 0):
            if (lastCone != None):
                coneCaminho(lastCone['x'] + (lastCone['w']/2))
        else:
            maior = cones[0]
            for cone in cones:
                if (cone['h'] > maior['h']):
                    maior = cone
            coneCaminho(maior['x'] + (maior['w']/2))
            lastCone = maior    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
