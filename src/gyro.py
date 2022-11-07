import smbus
from time import sleep
DEVICE_BUS = 1
GYRO_ADDRESS = 0x68

INIT_REGISTER = 0x6B
RANGE_REGISTER = 0x1B
BAND_WIDTH_REGISTER = 0X1A

RANGE_VALUE = 0b00001000 #valor para 500 g/s
BAND_WIDTH_VALUE = 0b00000100 #valor para 21Hz

GYRO_SCALE = 65.5
GYRO_CONSTANT = 0.017453293

i2c = smbus.SMBus(DEVICE_BUS)


i2c.write_byte_data(GYRO_ADDRESS, INIT_REGISTER, 0x00)
i2c.write_byte_data(GYRO_ADDRESS, RANGE_REGISTER, RANGE_VALUE)
i2c.write_byte_data(GYRO_ADDRESS, BAND_WIDTH_REGISTER, BAND_WIDTH_VALUE)

def readAngularSpeed():
  rawXLOW = i2c.read_byte_data(GYRO_ADDRESS, 0x43)
  rawXLHIGH = i2c.read_byte_data(GYRO_ADDRESS, 0x43)
  rawX = rawXLOW | rawXLHIGH

  gyroX = (float(rawX) / GYRO_SCALE) * GYRO_CONSTANT

  return gyroX

if (__name__ == '__main__'):
    while(True):
      gyro = readAngularSpeed()
      print(gyro)
