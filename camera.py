import time
import picamera
import RPi.GPIO as GPIO

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

# Continuously check if the button is pressed
while True:
    if GPIO.input(24) == GPIO.LOW:
        take_picture()
        time.sleep(0.2)
