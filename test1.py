import speech_recognition as sr
import board
import busio
import adafruit_ssd1306
import pyaudio
from PIL import Image, ImageDraw, ImageFont

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1306 OLED class.
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear the OLED display buffer.
oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on the image.
draw = ImageDraw.Draw(image)

# Load default font.
font = ImageFont.load_default()

# Display message on OLED display
draw.text((0, 0), "Say something!", font=font, fill=255)
oled.image(image)
oled.show()

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone(sample_rate=44100, chunk_size=512) as source:
    r.adjust_for_ambient_noise(source, duration=0.5)
    while True:
        audio = r.listen(source)
        try:
            recognized_text = r.recognize_google(audio)
            # Clear the OLED display buffer.
            oled.fill(0)
            # Display recognized text on OLED display
            draw.text((0, 0), recognized_text, font=font, fill=255)
            oled.image(image)
            oled.show()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))