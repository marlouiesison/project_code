import speech_recognition as sr
import board
import busio
import adafruit_ssd1306
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

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Google Speech Recognition
try:
    recognized_text = r.recognize_google(audio)
    print("Google Speech Recognition thinks you said: " + recognized_text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
    recognized_text = "Could not understand audio"
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    recognized_text = "Could not request results from Google Speech Recognition service"

# Draw the recognized text on the OLED display.
draw.text((0, 0), recognized_text, font=font, fill=255)

# Display image on the OLED.
oled.image(image)
oled.show()

