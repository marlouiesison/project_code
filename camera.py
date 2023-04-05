import board
import busio
import adafruit_ssd1306
import time
import datetime
from PIL import Image, ImageDraw, ImageFont
import picamera
import RPi.GPIO as GPIO

# Set up OLED display
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=None)
pic= "Pic!"


# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Create a function to take a picture
def take_picture():
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(1)
        timestamp = time.strftime('%Y%m%d%H%M%S')
        filename = '/home/pi/image_{}.jpg'.format(timestamp)
        camera.capture(filename)
        camera.stop_preview()
        print("Picture taken!")

# Continuously listen for and transcribe speech
while True:
    # Continuously check if the button is pressed
    if GPIO.input(24) == GPIO.LOW:
        take_picture()
        oled.fill(0)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((50, 50), pic, font=font, fill=255)
        oled.image(image)
        oled.show()
        time.sleep(0.2)
