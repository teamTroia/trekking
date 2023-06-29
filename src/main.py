import numpy as np
import random as rng
import time
import cv2
from visao import procuraCONE
import serial

MARGEM_ERRO_CENTRO = 60

# desliga o LED
def offLED(pino):
    time.sleep(1)
    GPIO.output(pino, GPIO.LOW)

# se cone na esquerda
def coneSentido(eixoX,arduino):
    arduino.write(str(eixoX).encode())
    
# liga os LED
#def ligaLED(eixoX):
#    GPIO.output(eixoX, GPIO.HIGH)
#    offLED(eixoX)

# define onde o cone está
def coneCaminho(eixoX,arduino):
    if eixoX > 320 + MARGEM_ERRO_CENTRO:
        print("Direita")
        coneSentido(eixoX,arduino)
    elif eixoX < 320 - MARGEM_ERRO_CENTRO:
        print("Esquerda")
        coneSentido(eixoX,arduino)
    else:
        print("Frente")
        coneSentido(eixoX,arduino)
        
    print('EixoX: ')
    print(eixoX)

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
           arduino = serial.Serial('/dev/ttyACM0', 9600)
           print('Arduino conectado')
           break
       except:
           print('Não passou')
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
         print("lens")
           #enableMotors(0,0)
       else:
           maior = cones[0]
           coneCaminho(maior['x'],arduino)
           print(maior['x'])
   cap.release()
   cv2.destroyAllWindows()
