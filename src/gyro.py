import smbus2 as smbus
from time import sleep

DEVICE_BUS = 1
GYRO_ADDRESS = 0x68

INIT_REGISTER = 0x6B
RANGE_REGISTER = 0x1B
BAND_WIDTH_REGISTER = 0X1A
INT_ENABLE = 0x38

RANGE_VALUE = 0b00001000 #valor para 500 g/s
BAND_WIDTH_VALUE = 0b00000100 #valor para 21Hz

GYRO_SCALE = 65.5
GYRO_CONSTANT = 0.017453293

i2c = smbus.SMBus(DEVICE_BUS)
sleep(1)

i2c.write_byte_data(GYRO_ADDRESS, INIT_REGISTER, 0x00)
i2c.write_byte_data(GYRO_ADDRESS, RANGE_REGISTER, RANGE_VALUE)
i2c.write_byte_data(GYRO_ADDRESS, BAND_WIDTH_REGISTER, BAND_WIDTH_VALUE)
#i2c.write_byte_data(GYRO_ADDRESS, INT_ENABLE, 1)
def readAngularSpeed():
  rawX = (i2c.read_byte_data(GYRO_ADDRESS, 0x43) << 8) | i2c.read_byte_data(GYRO_ADDRESS, 0x44)
  rawY = (i2c.read_byte_data(GYRO_ADDRESS, 0x45) << 8) | i2c.read_byte_data(GYRO_ADDRESS, 0x46)
  rawZ = (i2c.read_byte_data(GYRO_ADDRESS, 0x47) << 8) | i2c.read_byte_data(GYRO_ADDRESS, 0x48)

  rawX = rawX if (rawX < 32768) else rawX - 65536
  rawY = rawY if (rawY < 32768) else rawY - 65536
  rawZ = rawZ if (rawZ < 32768) else rawZ - 65536
  
  gyroX = float(rawX) / GYRO_SCALE
  gyroY = float(rawY) / GYRO_SCALE
  gyroZ = float(rawZ) / GYRO_SCALE

  gyroX *= GYRO_CONSTANT
  gyroY *= GYRO_CONSTANT
  gyroZ *= GYRO_CONSTANT

  return {'x': gyroX, 'y': gyroY, 'z': gyroZ}

if (__name__ == '__main__'):
    while(True):
      gyro = readAngularSpeed()
      print(f"x: {gyro['x']:.6f}, y: {gyro['y']:.6f}, z: {gyro['z']:.6f}")
      
