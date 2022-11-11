import numpy as np
import random as rng
import RPi.GPIO as GPIO
import time
import cv2
from control import enableMotors
from visao import procuraCONE

MARGEM_ERRO_CENTRO = 60

# desliga o LED
def offLED(pino):
    time.sleep(1)
    GPIO.output(pino, GPIO.LOW)

# se cone na esquerda
def coneESQ():
    print('O cone esta na esquerda')
    enableMotors(30, 0.3)

# se cone na direita
def coneDIR():
    print('O cone esta na direita')
    enableMotors(30, -0.3)

# se cone em frente
def coneFRE(speed = 60):
    print('O cone esta em frente')
    enableMotors(60, 0)
    

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
    maiorTodos = None
    while(1):
        cones = procuraCONE(cap)
        
        if (len(cones) == 0):
            coneFRE()
            #enableMotors(0,0)
        else:
            maior = cones[0]
            for cone in cones:
                if (cone['h'] > maior['h']):
                    maior = cone
            if (maiorTodos == None or maior['h'] >= maiorTodos * 0.8):
                coneCaminho(maior['x'] + (maior['w']/2))
                maiorTodos = maior['h']
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
