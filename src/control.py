from gyro import readAngularSpeed
from motor import enablePKS1, enablePKS2
import time
BASE_SPEED = 25
MIN_SPEED = 0

def controlMotor(left, right):
  absoluteRight = abs(right)
  rightSignal = right / absoluteRight

  absoluteLeft = abs(left)
  leftSignal = left / absoluteLeft

  enablePKS1((absoluteRight/100) * BASE_SPEED, rightSignal)
  enablePKS2((absoluteLeft/100) * BASE_SPEED, leftSignal)

def pid(target, actual):
  kp = 20
  kd = 0
  ki = 0

  error = target - actual
  output = error * kp

  return output 

def enableMotors(linear, angular):
  gyro = readAngularSpeed()
  angularSpeed = pid(angular, gyro['z'])
  print(angularSpeed)
  angularSpeed = 100 if (angularSpeed > 100) else 100

  leftSpeed = linear - angular
  rightSpeed = linear + angular

  leftSpeed = 0 if (abs(leftSpeed) < MIN_SPEED) else leftSpeed
  rightSpeed = 0 if (abs(rightSpeed) < MIN_SPEED) else rightSpeed

  controlMotor(leftSpeed, rightSpeed)

if (__name__ == '__main__'):
    while(1):
        enableMotors(100,0)
