import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

import speech_recognition as sr
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech
import time
import RPi.GPIO as GPIO
import audioio
import digitalio


# Set up OLED display
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=None)


# Set up Google credentials and client
creds = service_account.Credentials.from_service_account_file('/home/pi/api_key/....json')
client = speech.SpeechClient(credentials=creds)

# Set up speech recognition
r = sr.Recognizer()

# Set up I2S microphone
#BCLK = board.D22
#LRCLK = board.D24
#DIN = board.D25
#MIC_EN = board.D27
SAMPLE_RATE = 16000

# Set up I2S microphone
BCLK = board.D18  # BCM 18
LRCLK = board.D19  # BCM 19
DIN = board.D20  # BCM 20
MIC_EN = board.D21  # BCM 21


mic = audioio.I2SOut(bit_clock=BCLK, word_clock=LRCLK, data=DIN, mode=audioio.I2S.PHILIPS, sample_rate=SAMPLE_RATE, data_format=audioio.I2S.MONO)

mic_enable = digitalio.DigitalInOut(MIC_EN)
mic_enable.direction = digitalio.Direction.OUTPUT
mic_enable.value = True

# Continuously listen for and transcribe speech
while True:
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)  # adjust for ambient noise
            oled.fill(0)  # clear OLED display
            
            # Create blank image for drawing.
            image = Image.new("1", (oled.width, oled.height))
            
            # Get drawing object to draw on the image.
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()

            draw.text((0, 0), 'Say something!', font=font, fill=255)
            oled.image(image)
            oled.show()
            
            audio = audioio.AudioIn(DIN, sample_rate=SAMPLE_RATE, data_format=audioio.AudioIn.MS2SB, channel_count=1)

            with audio:
                audio_length = 0
                buffer_size = 512
                while audio_length < 5 * SAMPLE_RATE:
                    buffer = bytearray(buffer_size)
                    num_bytes_read = audio.readinto(buffer)
                    audio_length += num_bytes_read // 2
                    mic.write(buffer)

            # recognize speech using Google Speech Recognition
            text = r.recognize_google_cloud(audio, credentials_json=creds)

            # display transcription on OLED display
            draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0) # clear screen
            draw.text((0, 0), text, font=font, fill=255)
            oled.image(image)
            oled.show()
            
        # wait a second before listening again
        time.sleep(1)
        
    except sr.UnknownValueError:
        # display error message on OLED display if speech cannot be transcribed
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0) # clear screen
        draw.text((0, 0), 'Could not understand', font=font, fill=255)
        oled.image(image)
        oled.show()
        print('Error: Could not understand speech')

    except sr.Request
