import numpy as np
import cv2
import random as rng
import RPi.GPIO as GPIO
import time

# desliga o LED
def offLED(pino):
    time.sleep(1)
    GPIO.output(pino, GPIO.LOW)

# se cone na esquerda
def coneESQ(eixoX):
    print('O cone esta na esquerda')
    ligaLED(eixoX)

# se cone na direita
def coneDIR(eixoX):
    print('O cone esta na direita')
    ligaLED(eixoX)

# se cone em frente
def coneFRE(eixoX):
    print('O cone esta em frente')
    ligaLED(eixoX)

# liga os LED
def ligaLED(eixoX):
    GPIO.output(eixoX, GPIO.HIGH)
    offLED(eixoX)

# define onde o cone está
def coneCaminho(eixoX):
    if eixoX > 340:
        coneDIR(21)
    elif eixoX < 300:
        coneESQ(18)
    else:
        coneFRE(20)
    if eixoX == None:
        print('None')
    else:
        print(eixoX)

# read until video is completed
def procuraCONE(frame):
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

    # smooth the image with erosion, dialation, and smooth gaussian
    smoothed_img = cv2.dilate(threshed_img, kernel, iterations = 13)
    smoothed_img = cv2.erode(smoothed_img, kernel, iterations = 13)

    # detect all edges witin the image
    edges_img = cv2.Canny(smoothed_img, 100, 200)
    contours, hierarchy = cv2.findContours(edges_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # set parameters for writing text and drawing lines
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 2
    fontColor = (0, 0, 255)
    lineType = 2

    # analyze each contour and deterime if it is a triangle
    for cnt in contours:
        boundingRect = cv2.boundingRect(cnt)
        approx = cv2.approxPolyDP(cnt, 0.06 * cv2.arcLength(cnt, True), True)
        # if the contour is a triangle, draw a bounding box around it and tag a traffic_cone label to it
        if len(approx) == 3:
            x, y, w, h = cv2.boundingRect(approx)
            rect = (x, y, w, h)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            coneCaminho(x)
            bottomLeftCornerOfText = (x, y)
            cv2.putText(frame,'traffic_cone', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)

    # display the resulting frame
    cv2.imshow('Frame',frame)

# closes all the frames
cv2.destroyAllWindows()

# func main
def main():
    cap = cv2.VideoCapture(0)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    
    # check if camera opened successfully
    if (cap.isOpened()== False): 
          print("Error opening video stream or file")

    print('iniciou')
    while(cap.isOpened()):

        # capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            procuraCONE(frame)

            # press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # break the loop
        else: 
            break

    # when everything done, release the video capture object
    cap.release()

if __name__ == '__main__':
    main()
