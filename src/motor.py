import RPi.GPIO as gpio
import time
 
gpio.setwarnings(False)

## pwms 12, 32, 33, 35
SD1_PKS1 = 12
IN1_PKS1 = 13
SD2_PKS1 = 32
IN2_PKS1 = 16

SD1_PKS2 = 33
IN1_PKS2 = 15
SD2_PKS2 = 35
IN2_PKS2 = 18

LED_OUT = 22

gpio.setmode(gpio.BOARD)
gpio.setup(SD1_PKS1,gpio.OUT)
gpio.setup(SD2_PKS1,gpio.OUT)
gpio.setup(SD1_PKS2,gpio.OUT)
gpio.setup(SD2_PKS2,gpio.OUT)

gpio.setup(IN1_PKS1,gpio.OUT)
gpio.setup(IN2_PKS1,gpio.OUT)
gpio.setup(IN1_PKS2,gpio.OUT)
gpio.setup(IN2_PKS2,gpio.OUT)

gpio.setup(LED_OUT, gpio.OUT)

gpio.output(LED_OUT, gpio.LOW)
pwmSD1_PKS1 = gpio.PWM(SD1_PKS1, 500)
pwmSD2_PKS1 = gpio.PWM(SD2_PKS1, 500)
pwmSD1_PKS2 = gpio.PWM(SD1_PKS2, 500)
pwmSD2_PKS2 = gpio.PWM(SD2_PKS2, 500)

pwmSD1_PKS1.start(0)
pwmSD2_PKS1.start(0)
pwmSD1_PKS2.start(0)
pwmSD2_PKS2.start(0)

gpio.output(IN1_PKS1, gpio.LOW)
gpio.output(IN2_PKS1, gpio.LOW)
gpio.output(IN1_PKS2, gpio.LOW)
gpio.output(IN2_PKS2, gpio.LOW)

def enablePKS1(dutyCycle, direction):
  if (direction == 1):
    pwmSD1_PKS1.ChangeDutyCycle(dutyCycle)
    pwmSD2_PKS1.ChangeDutyCycle(100)
    gpio.output(IN1_PKS1, gpio.HIGH)
    gpio.output(IN2_PKS1, gpio.LOW)
  elif (direction == -1):
    pwmSD2_PKS1.ChangeDutyCycle(dutyCycle)
    pwmSD1_PKS1.ChangeDutyCycle(100)
    gpio.output(IN1_PKS1, gpio.LOW)
    gpio.output(IN2_PKS1, gpio.HIGH)
  else:
    pwmSD2_PKS1.ChangeDutyCycle(0)
    pwmSD1_PKS1.ChangeDutyCycle(0)
    gpio.output(IN1_PKS1, gpio.LOW)
    gpio.output(IN2_PKS1, gpio.LOW)

def enablePKS2(dutyCycle, direction):
  if (direction == -1):
    pwmSD1_PKS2.ChangeDutyCycle(dutyCycle)
    pwmSD2_PKS2.ChangeDutyCycle(100)
    gpio.output(IN1_PKS2, gpio.HIGH)
    gpio.output(IN2_PKS2, gpio.LOW)
  elif (direction == 1):
    pwmSD2_PKS2.ChangeDutyCycle(dutyCycle)
    pwmSD1_PKS2.ChangeDutyCycle(100)
    gpio.output(IN1_PKS2, gpio.LOW)
    gpio.output(IN2_PKS2, gpio.HIGH)
  else:
    pwmSD2_PKS2.ChangeDutyCycle(0)
    pwmSD1_PKS2.ChangeDutyCycle(0)
    gpio.output(IN1_PKS2, gpio.LOW)
    gpio.output(IN2_PKS2, gpio.LOW)

def blinkLed():
    gpio.output(LED_OUT, gpio.HIGH)
    time.sleep(0.5)
    gpio.output(LED_OUT, gpio.LOW)
    time.sleep(0.5)
    gpio.output(LED_OUT, gpio.HIGH)
    time.sleep(0.5)
    gpio.output(LED_OUT, gpio.LOW)
    time.sleep(0.5)
    gpio.output(LED_OUT, gpio.HIGH)
    time.sleep(0.5)
    gpio.output(LED_OUT, gpio.LOW)

if __name__ == '__main__':
  while(1):
    enablePKS2(20,1)
    enablePKS1(20,1)

