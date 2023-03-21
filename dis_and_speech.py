import board
#from board import SCL, SDA
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

import speech_recognition as sr
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech
import time
#import gpiozero
import RPi.GPIO as GPIO

# Set up OLED display
i2c = busio.I2C(board.SCL, board.SDA)
#oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
#oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C, external_vcc=False, reset=None, gpio=GPIO, framebuffer=None, font_path='/home/pi/font5x8.bin')
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=None)


#font_path="/home/pi/font5x8.bin"
#font=None

# Set up Google credentials and client
creds = service_account.Credentials.from_service_account_file('/home/pi/api_key/....json')
client = speech.SpeechClient(credentials=creds)

# Set up speech recognition
r = sr.Recognizer()
mic = sr.Microphone()

# Continuously listen for and transcribe speech
while True:
    with mic as source:
        r.adjust_for_ambient_noise(source)  # adjust for ambient noise
        oled.fill(0)  # clear OLED display
        oled.show()
        
        # Create blank image for drawing.
        image = Image.new("1", (oled.width, oled.height))
        
        # Get drawing object to draw on the image.
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        oled.text('Say something!', 0, 0, 1)  # display message on OLED display
        #oled.show()
        draw.text((0, 0, 1), 'Say something!', font=font, fill=255)
        oled.image(image)
        oled.show()
        
        audio = r.listen(source)

    try:
        # recognize speech using Google Speech Recognition
        text = r.recognize_google_cloud(audio, credentials_json=creds)

        # display transcription on OLED display
        oled.fill(0)
        oled.text(text, 0, 0, 1)
        oled.show()
        
    except sr.UnknownValueError:
        # display error message on OLED display if speech cannot be transcribed
        oled.fill(0)
        oled.text('Could not', 0, 0, 1)
        oled.text('understand', 0, 10, 1)
        oled.show()
        print('Error: Could not understand speech')

        
    except sr.RequestError as e:
        # display error message on OLED display if there is an error with the API
        oled.fill(0)
        oled.text('API error:', 0, 0, 1)
        oled.text(str(e), 0, 10, 1)
        oled.show()
        print('Error: API request error -', e)

    # wait a second before listening again
    time.sleep(1)

