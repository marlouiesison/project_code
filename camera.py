import time
import picamera

# Create a function to take a picture
def take_picture():
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        timestamp = time.strftime('%Y%m%d%H%M%S')
        filename = '/home/pi/image_{}.jpg'.format(timestamp)
        camera.capture(filename)
        camera.stop_preview()
        print("Picture taken and saved as: {}".format(filename))

# Call the take_picture function
take_picture()
