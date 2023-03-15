
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

# Draw some text.
text = "Hello, world!"
draw.text((0, 0), text, font=font, fill=255)

# Display image on the OLED.
oled.image(image)
oled.show()

