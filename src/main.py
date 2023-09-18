import numpy as np
import random as rng
import time
import cv2
from visao import procuraCONE
import serial

MARGEM_ERRO_CENTRO = 60

# se cone na esquerda
def coneESQ(eixoX,arduino):
    arduino.write(str(-eixoX).encode())
    

# se cone na direita
def coneDIR(eixoX,arduino):
    arduino.write(str(eixoX).encode())
    

# se cone em frente
def coneFRE(speed,arduino):
    arduino.write('1'.encode())

# define onde o cone está
def coneCaminho(eixoX,arduino):
    if eixoX > 320 + MARGEM_ERRO_CENTRO:
        coneDIR(eixoX,arduino)
    elif eixoX < 320 - MARGEM_ERRO_CENTRO:
        coneESQ(eixoX,arduino)
    else:
        coneFRE(eixoX,arduino)

def onTrackBarBrilho(value):
   global brilho
   brilho = value

def onTrackBarSaturacao(value):
   global saturacao
   saturacao = value

if __name__ == '__main__':
    brilho = 0
    saturacao = 0

    while True:
        try:  #Tenta se conectar, se conseguir, o loop se encerra
            arduino = serial.Serial('COM3', 9600)
            print('Arduino conectado')
            break
        except:
            pass
    
    cap = cv2.VideoCapture(0)
    
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    lastCone = None
    maiorTodos = None

    cv2.namedWindow("Configuracao")
    cv2.createTrackbar("Brilho   ", "Configuracao", 0, 255, onTrackBarBrilho)
    cv2.createTrackbar("Saturacao", "Configuracao", 0, 255, onTrackBarSaturacao)

    while(1):
        cones = procuraCONE(cap, brilho, saturacao)
        if (len(cones) == 0):
            coneFRE(60,arduino)
        else:
            maior = cones[0]
            for cone in cones:
                if (cone['h'] > maior['h']):
                    maior = cone
            if (maiorTodos == None or maior['h'] >= maiorTodos * 0.8):
                coneCaminho(maior['x'] + (maior['w']/2),arduino)
                maiorTodos = maior['h']
    cap.release()
    cv2.destroyAllWindows()
