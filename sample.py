import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech
import time
import audioio
import digitalio

# Set up OLED display
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=None)

# Set up Google credentials and client
creds = service_account.Credentials.from_service_account_file('/home/pi/api_key/....json')
client = speech.SpeechClient(credentials=creds)

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

# Set up PIL image and font
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Continuously listen for and transcribe speech
while True:
    try:
        # Read audio from I2S microphone
        audio = audioio.AudioIn(DIN, sample_rate=SAMPLE_RATE, data_format=audioio.AudioIn.MS2SB, channel_count=1)

        with mic, audio:
            audio_length = 0
            buffer_size = 512
            while audio_length < 5 * SAMPLE_RATE:
                buffer = bytearray(buffer_size)
                num_bytes_read = audio.readinto(buffer)
                audio_length += num_bytes_read // 2
                mic.write(buffer)

                # Transcribe speech using Google Cloud Speech-to-Text API
                content = buffer
                audio = speech.RecognitionAudio(content=content)
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=SAMPLE_RATE,
                    language_code="en-US",
                )

                response = client.recognize(request={"config": config, "audio": audio})

                for result in response.results:
                    transcript = result.alternatives[0].transcript

             
                    # Clear OLED display
                    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

                    # Display transcription on OLED
                    draw.text((0, 0), transcript, font=font, fill=255)
                    oled.image(image)
                    oled.show()

                    # Wait briefly before clearing display and continuing to listen
                    time.sleep(0.5)
                    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

