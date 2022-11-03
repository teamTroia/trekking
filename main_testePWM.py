# Este eh um teste de bancada para deteccao dos limites a serem verificados para acionamento
import RPi.GPIO as GPIO
from time import sleep 
'''
def testeCoordenadas(eixoX):
    if eixoX >= 340:i
        print('O cone esta a direita, viranduuu...')
    elif eixoX <= 300:
        print('O cone esta a esquerda, viranduuu...')
    else:
        print('Ovo reto fodase')
'''

GPIO.setmode(GPIO.BOARD)

# Setup GPIO Pins
GPIO.setup(12, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)

# Set PWM instance and their frequency
pwm12 = GPIO.PWM(12, 8000)
pwm32 = GPIO.PWM(32, 8000)
pwm33 = GPIO.PWM(33, 8000)
pwm35 = GPIO.PWM(35, 8000)

print("pwm 50")
pwm32.start(100)
pwm12.start(50)
pwm33.start(0)
pwm35.start(0)
sleep(10)
print("pwm 25")
pwm12.ChangeDutyCycle(25)
sleep(10)
print("pwm 100")
pwm12.ChangeDutyCycle(70)
sleep(10)
print("parou")
pwm12.stop()
