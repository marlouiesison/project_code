import board
import busio
import adafruit_ssd1306
import time
import datetime
from PIL import Image, ImageDraw, ImageFont

import speech_recognition as sr
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech

import adafruit_micropython_blinka.terminal as terminal
from adafruit_circuitpython_busdevice.i2s import I2SIn

# Set up OLED display
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=None)

# Set up Google credentials and client
creds = service_account.Credentials.from_service_account_file('/home/pi/api_key/....json')
client = speech.SpeechClient(credentials=creds)

# Set up speech recognition
r = sr.Recognizer()
mic = I2SIn(board.I2S_DOUT, board.I2S_BCLK, board.I2S_LRCLK)

# Set up initial display message
date_string = ''
time_string = ''
speech_text = ''
message = 'Say something!'

# Continuously listen for and transcribe speech
while True:
    with mic as source:
        r.adjust_for_ambient_noise(source)  # adjust for ambient noise
        oled.fill(0)  # clear OLED display
        
        # Create blank image for drawing.
        image = Image.new("1", (oled.width, oled.height))
        
        # Get drawing object to draw on the image.
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        # Update date and time strings
        now = datetime.datetime.now()
        new_date_string = now.strftime("%a, %b %d %Y")
        new_time_string = now.strftime("%I:%M %p")
        
        # Update display message with speech text or date and time strings
        if speech_text:
            message = speech_text
        else:
            message = ' '.join([new_date_string, new_time_string])
        
        # Draw message on OLED display
        draw.text((0, 0), message, font=font, fill=255)
        oled.image(image)
        oled.show()
        
        audio = r.listen(source)

    try:
        # recognize speech using Google Speech Recognition
        text = r.recognize_google_cloud(audio, credentials_json=creds)
        
        # Update speech text with transcribed text
        speech_text = text

    except sr.UnknownValueError:
        # display error message on OLED display if speech cannot be transcribed
        speech_text = ''
        
    except sr.RequestError as e:
        # display error message on OLED display if there is an error with the API
        speech_text = 'API error: ' + str(e)

    # wait a short time before listening again
    time.sleep(0.1)
