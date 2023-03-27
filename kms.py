import board
import busio
import digitalio
import adafruit_ssd1306
import speech_recognition as sr
from PIL import Image, ImageDraw, ImageFont

# Set up OLED display
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Set up I2S MEMS microphone breakout
mic_clock = digitalio.DigitalInOut(board.D18)
mic_data = digitalio.DigitalInOut(board.D20)
mic_clock.direction = digitalio.Direction.INPUT
mic_data.direction = digitalio.Direction.INPUT

# Set up speech recognition
r = sr.Recognizer()

# Set up font and image
font = ImageFont.load_default()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

while True:
    # Read audio data from I2S MEMS microphone breakout
    audio_data = bytearray(320)
    for i in range(len(audio_data)):
        audio_data[i] = mic_data.value
        while not mic_clock.value:
            pass
        while mic_clock.value:
            pass
    
    # Convert audio data to audio source for speech recognition
    audio_source = sr.AudioData(audio_data, sample_rate=16000, sample_width=2)

    try:
        # Recognize speech
        text = r.recognize_google(audio_source)

        # Display recognized text on OLED display
        oled.fill(0)
        draw.text((0, 0), text, font=font, fill=1)
        oled.image(image)
        oled.show()

    except sr.UnknownValueError:
        # Display error message if speech cannot be recognized
        oled.fill(0)
        draw.text((0, 0), "Unknown Value Error", font=font, fill=1)
        oled.image(image)
        oled.show()

    except sr.RequestError as e:
        # Display error message if there is an error with the API
        oled.fill(0)
        draw.text((0, 0), f"Request Error: {e}", font=font, fill=1)
        oled.image(image)
        oled.show()

        
        
        
        
#this IS A BRAND NEW CODE: WILL NOT RUN
##############
import board
import busio
import adafruit_ssd1306
import time
import datetime
from PIL import Image, ImageDraw, ImageFont

import speech_recognition as sr
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech
import RPi.GPIO as GPIO

# Set up OLED display
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=None)

# Set up Google credentials and client
creds = service_account.Credentials.from_service_account_file('/home/pi/api_key/....json')
client = speech.SpeechClient(credentials=creds)

# Set up speech recognition
r = sr.Recognizer()

# Set up mems microphone
sample_rate = 16000
channel_count = 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(20, GPIO.IN)
GPIO.output(12, GPIO.LOW)
GPIO.output(19, GPIO.LOW)

# Set up initial display message
date_string = ''
time_string = ''
speech_text = ''
message = 'Say something!'

# Set up font and image
font = ImageFont.load_default()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Continuously listen for and transcribe speech
while True:
    with sr.Microphone(sample_rate=sample_rate, channel_count=channel_count, device_index=None, input=True, frames_per_buffer=320, resume=True) as source:
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(19, GPIO.HIGH)
        r.adjust_for_ambient_noise(source)  # adjust for ambient noise
        oled.fill(0)  # clear OLED display
        
        # Update date and time strings
        now = datetime.datetime.now()
        new_date_string = now.strftime("%a, %b %d %Y")
        new_time_string = now.strftime("%I:%M %p")
        
        # Get drawing object to draw on the image.
        draw = ImageDraw.Draw(image)
        
        # Update display message with speech text or date and time strings
        if speech_text:
            message = speech_text
            draw.text((0, 0), message, font=font, fill=255)
        else:
            message = ' '.join([new_date_string, new_time_string])
            draw.text((0, 0), message, font=font, fill=255)
        
        # Display message on OLED display
        oled.image(image)
        oled.show()
        
        # Listen for speech and transcribe it
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

    finally:
       
