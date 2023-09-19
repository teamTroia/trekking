import cv2
import numpy as np

def procuraCONE(cap, brilho, saturacao):
  while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
      hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      lower_orange1 = np.array([0, 60, 80])
      lower_orange2 = np.array([10, saturacao, brilho])
      upper_orange1 = np.array([0, 60, 80])
      upper_orange2 = np.array([10, saturacao, brilho])

      masc_Laranja = cv2.inRange(hsv_img, lower_orange1, upper_orange2)
      kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
      masc_Laranja = cv2.morphologyEx(masc_Laranja, cv2.MORPH_OPEN, kernel)
      contours, hierarchy = cv2.findContours(masc_Laranja, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      font = cv2.FONT_HERSHEY_SIMPLEX
      fontScale = 2
      fontColor = (0, 0, 255)
      lineType = 2
      cones = []
      for cnt in contours:
          boundingRect = cv2.boundingRect(cnt)
          approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
          if len(approx) == 3:
              x, y, w, h = cv2.boundingRect(approx)
              cones.append({'x':x, 'y': y, 'w': w, 'h': h})
              rect = (x, y, w, h)
              cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
              bottomLeftCornerOfText = (x, y)
              cv2.putText(frame,'traffic_cone', 
                  bottomLeftCornerOfText, 
                  font, 
                  fontScale,
                  fontColor,
                  lineType)

      cv2.imshow('Frame',frame)
      if cv2.waitKey(25) & 0xFF == ord('q'):
        break
      return cones
    else: 
      break

def onTrackBarBrilho(value):
   global brilho
   brilho = value

def onTrackBarSaturacao(value):
   global saturacao
   saturacao = value

if __name__ == '__main__':
  cap = cv2.VideoCapture(0)
  
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
  
  brilho = 0
  saturacao = 0

  cv2.namedWindow("Configuracao")
  cv2.createTrackbar("Brilho   ", "Configuracao", 0, 255, onTrackBarBrilho)
  cv2.createTrackbar("Saturacao", "Configuracao", 0, 255, onTrackBarSaturacao)

  while(1):
    cones = procuraCONE(cap, brilho, saturacao)
    print(cones)
