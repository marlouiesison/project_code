import board
import busio
import adafruit_lis2dh12

i2c = busio.I2C(board.SCL, board.SDA)
lis2dh12 = adafruit_lis2dh12.LIS2DH12(i2c)

while True:
    x, y, z = lis2dh12.acceleration
    print((x, y, z))