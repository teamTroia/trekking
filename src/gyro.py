import smbus

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
  gyro_raw_data = i2c.read_i2c_block_data(GYRO_ADDRESS, 0X43, 6)
  rawX = gyro_raw_data[0] | gyro_raw_data[1]
  rawY = gyro_raw_data[2] | gyro_raw_data[3]
  rawZ = gyro_raw_data[4] | gyro_raw_data[5]

  gyroX = (rawX / GYRO_SCALE) * GYRO_CONSTANT
  gyroY = (rawY / GYRO_SCALE) * GYRO_CONSTANT
  gyroZ = (rawZ / GYRO_SCALE) * GYRO_CONSTANT

  return {'x': gyroX, 'y': gyroY, 'z': gyroZ}

if (__name__ == '__main__'):
  while(1):
    gyro = readAngularSpeed()
    print(gyro)
