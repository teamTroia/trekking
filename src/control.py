from gyro import readAngularSpeed
from motor import enablePKS1, enablePKS2

BASE_SPEED = 10
MIN_SPEED = 0

def controlMotor(left, right):
  absoluteRight = abs(right)
  rightSignal = right / absoluteRight

  absoluteLeft = abs(left)
  leftSignal = left / absoluteLeft

  enablePKS1((absoluteLeft/100) * BASE_SPEED, leftSignal)
  enablePKS2((absoluteRight/100) * BASE_SPEED, rightSignal)

def pid(target, actual):
  kp = 20
  kd = 0
  ki = 0

  error = target - actual
  output = error * kp

  return output 

def enableMotors(linear, angular):
  angularSpeed = pid(angular, readAngularSpeed()['z'])
  angularSpeed = 100 if (angularSpeed > 100) else 100

  leftSpeed = linear - angular
  rightSpeed = linear + angular

  leftSpeed = 0 if (abs(leftSpeed) < MIN_SPEED) else leftSpeed
  rightSpeed = 0 if (abs(rightSpeed) < MIN_SPEED) else rightSpeed

  controlMotor(leftSpeed, rightSpeed)