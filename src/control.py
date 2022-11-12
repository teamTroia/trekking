from gyro import readAngularSpeed
from motor import enablePKS1, enablePKS2
import time

BASE_SPEED = 0.40
MIN_SPEED = 0

def controlMotor(left, right):
  absoluteRight = abs(right)
  rightSignal = 1 if absoluteRight == 0 else right / absoluteRight

  absoluteLeft = abs(left)
  leftSignal = 1 if absoluteLeft == 0 else left / absoluteLeft
  print(f"absleft: {left} {absoluteLeft} {leftSignal} absright: {right} {absoluteRight} {rightSignal}")
  enablePKS1(absoluteRight * BASE_SPEED, rightSignal*-1)
  enablePKS2(absoluteLeft * BASE_SPEED, leftSignal*-1)

def pid(target, actual):
  kp = 65
  kd = 0
  ki = 0

  error = target - actual
  output = error * kp

  return output 

def enableMotors(linear, angular):
  gyro = readAngularSpeed()
  angularSpeed = pid(angular, gyro['z'])
  #print(angularSpeed)
  angularSpeed = 100 if (angularSpeed > 100) else angularSpeed

  leftSpeed = linear + angularSpeed
  rightSpeed = linear - angularSpeed

  leftSpeed = 0 if (abs(leftSpeed) < MIN_SPEED) else leftSpeed
  rightSpeed = 0 if (abs(rightSpeed) < MIN_SPEED) else rightSpeed

  controlMotor(leftSpeed, rightSpeed)

if (__name__ == '__main__'):
    on = True
    while(on):
        try:
            enableMotors(60,0)
        except KeyboardInterrupt:
            on = False
        except:
            print("engasguei")
            
