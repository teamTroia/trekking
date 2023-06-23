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
      upper_orange2 = np.array([10,  saturacao, brilho])

      kernel = np.ones((5,5),np.uint8)
      imgThreshLow = cv2.inRange(hsv_img, lower_orange1, lower_orange2)
      imgThreshHigh = cv2.inRange(hsv_img, upper_orange1, upper_orange2)
    
      kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
      mascara_laranja = cv2.morphologyEx(mascara_laranja, cv2.MORPH_OPEN, kernel)

      contornos, _ = cv2.findContours(mascara_laranja, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      triangulos_laranjas = []

      smoothed_img = cv2.dilate(imgThreshHigh, kernel, iterations = 13)
      smoothed_img = cv2.erode(smoothed_img, kernel, iterations = 13)

      edges_img = cv2.Canny(smoothed_img, 100, 200)
      contours, hierarchy = cv2.findContours(edges_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

      font = cv2.FONT_HERSHEY_SIMPLEX
      fontScale = 2
      fontColor = (0, 0, 255)
      lineType = 2
      cones = []
      for cnt in contours:
        boundingRect = cv2.boundingRect(cnt)
        approx = cv2.approxPolyDP(cnt, 0.06 * cv2.arcLength(cnt, True), True)
        if len(approx) == 3:
          x, y, w, h = cv2.boundingRect(approx)
          cones.append({'x': x, 'y': y, 'w': w, 'h': h})
          rect = (x, y, w, h)
          cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
          bottomLeftCornerOfText = (x, y)
          cv2.putText(frame, 'traffic_cone',
                  bottomLeftCornerOfText,
                  font,
                  fontScale,
                  fontColor,
                  lineType)

        center_x = x + w // 2
        print(center_x)

      cv2.imshow('Frame', frame)
      
      return cones
    else: 
      break

def onTrackbarBrilho(value):
    global brilho
    brilho = value

def onTrackbarSaturacao(value):
    global saturacao
    saturacao = value
  
if __name__ == '__main__':

  cap = cv2.VideoCapture(0)
  
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
  cap.set(cv2.CAP_PROP_BRIGHTNESS, -34)
  cap.set(cv2.CAP_PROP_CONTRAST, 29)
  cap.set(cv2.CAP_PROP_SATURATION, 128)
  cap.set(cv2.CAP_PROP_GAIN, 54)
  cap.set(cv2.CAP_PROP_EXPOSURE, 157)
  cap.set(cv2.CAP_PROP_SHARPNESS, 3)
  cap.set(cv2.CAP_PROP_AUTO_WB, 0)
  cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4204)
  cap.set(cv2.CAP_PROP_HUE, 8)
  
  cv2.namedWindow("Configuração")
  cv2.createTrackbar("Brilho   ", "Configuração", 0, 255, onTrackbarBrilho);
  cv2.createTrackbar("Saturação", "Configuração", 0, 255, onTrackbarSaturacao);

  while(1):
    cones = procuraCONE(cap, brilho, saturacao)
    print(cones)
