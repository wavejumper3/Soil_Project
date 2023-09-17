import RPi.GPIO as GPIO
import time

# GPIO setup
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
	if GPIO.input(channel):
		print("No water detected.")
	else:
		print("Water detected.")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

# simple loop
while True:
	time.sleep(2.0)
