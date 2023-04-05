import RPi.GPIO as GPIO
import time
import picamera

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Create a function to take a picture
def take_picture():
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        camera.capture('/home/pi/image.jpg')
        camera.stop_preview()
        print("Picture taken!")

# Wait for the button to be pressed
while True:
    if GPIO.input(24) == GPIO.LOW:
        take_picture()
        time.sleep(0.2)
