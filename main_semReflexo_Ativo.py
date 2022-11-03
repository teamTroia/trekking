import numpy as np
import cv2
import random as rng
import RPi.GPIO as GPIO
import time
import trekking

# se cone na frente
def irRETO():
    print('To indo Reto')
    trekking.enablePKS1(50, 1)
    trekking.enablePKS2(50, -1)
    
    #while conePROXIMO() = False:
        #if conePROXIMO() = True:
            #pwm12.stop()
            #pwm36.stop()
    
# se cone na direita
def irDIR():
    print('To indo Direita')
    trekking.enablePKS1(50, 1)
    trekking.enablePKS2(75 ,-1)

# se cone na esquerda
def irESQ():
    print('To indo Esquerda')
    trekking.enablePKS1(75, 1)
    trekking.enablePSK2(50, -1)

# define onde o cone está
def coneCaminho(eixoX):
    if eixoX > 340:
        while procuraCONE() > 340: 
            irDIR()
        #pwm36.stop()
    elif eixoX < 300:
        while procuraCONE() < 300:
            irESQ()
        #pwm12.stop()
    else:
        irRETO()
        if eixoX == None:
            print('não tem')
        else:
            print(eixoX)

# read until video is completed
def procuraCONE():
    frame = cap.read()
    # convert the image to HSV because easier to represent color in
    # HSV as opposed to in BGR 
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of orange traffic cone color in HSV
    lower_orange1 = np.array([0, 135, 135])
    lower_orange2 = np.array([15, 255, 255])
    upper_orange1 = np.array([159, 135, 80])
    upper_orange2 = np.array([179, 255, 255])

    kernel = np.ones((5,5),np.uint8)
    # threshold the HSV image to get only bright orange colors
    imgThreshLow = cv2.inRange(hsv_img, lower_orange1, lower_orange2)
    imgThreshHigh = cv2.inRange(hsv_img, upper_orange1, upper_orange2)
   
    # Bitwise-OR low and high threshes
    threshed_img = cv2.bitwise_or(imgThreshLow, imgThreshHigh)

    # get rid of small artifacts that are not cones
    threshed_img = cv2.bitwise_and(threshed_img, imgThreshHigh)

    # # get rid of general small artifacts 
    # threshed_img_smooth = cv2.erode(threshed_img, kernel, iterations = 1)
    # threshed_img_smooth = cv2.dilate(threshed_img_smooth, kernel, iterations = 1)

    smoothed_img = cv2.dilate(threshed_img, kernel, iterations = 13)
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
            rect = (x, w, y, h)
            cones.append(rect)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            bottomLeftCornerOfText = (x, y)
            cv2.putText(frame,'traffic_cone', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
    cv2.imshow('Frame',frame)
    return x

# closes all the frames
cv2.destroyAllWindows()

# func main
def main():
    cap = cv2.VideoCapture(0)
    
    # check if camera opened successfully
    if (cap.isOpened()== False): 
          print("Error opening video stream or file")

    print('iniciou')
    while(cap.isOpened()):
        ret = cap.read()
        if ret == True:
            eixoX = procuraCONE()
            coneCaminho(eixoX)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else: 
            break
    cap.release()

if __name__ == '__main__':
    main()
