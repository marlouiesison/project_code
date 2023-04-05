import board
import busio
import adafruit_ssd1306
import time
import datetime
from PIL import Image, ImageDraw, ImageFont
import speech_recognition as sr
import picamera
import RPi.GPIO as GPIO

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up OLED display
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=None)

# Set up speech recognition
r = sr.Recognizer()
mic = sr.Microphone(sample_rate=16000, chunk_size=1024)

# Create a function to take a picture
def take_picture():
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        timestamp = time.strftime('%Y%m%d%H%M%S')
        filename = '/home/pi/image_{}.jpg'.format(timestamp)
        camera.capture(filename)
        camera.stop_preview()
        print("Picture taken!")

# Set up initial display message
date_string = ''
time_string = ''
speech_text = ''
message1 = 'Say something!'
message2 = ''
message3 = ''

# Continuously listen for and transcribe speech
while True:
    # Continuously check if the button is pressed
    if GPIO.input(24) == GPIO.LOW:
        take_picture()
        time.sleep(0.2)

    # Clear OLED display and update date and time strings
    oled.fill(0)
    now = datetime.datetime.now()
    date_string = now.strftime("%a, %b %d %Y")
    time_string = now.strftime("%I:%M %p")

    with mic as source:
        r.adjust_for_ambient_noise(source)  # adjust for ambient noise

        # Get drawing object to draw on the OLED display
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Display speech text if it exists, or default message if not
        if speech_text:
            lines = speech_text.split('\n')
            if len(lines) > 0:
                message1 = lines[0]
            if len(lines) > 1:
                message2 = lines[1]
            if len(lines) > 2:
                message3 = lines[2]    

            draw.text((0, 
