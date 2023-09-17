import RPi.GPIO as GPIO
import time
import board
# import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)
photo_pin = 17
GPIO.setup(photo_pin, GPIO.IN)

#Set the threshold value for sunlight detection
sunlight_threshold = 500

def get_light_intensity():
	#get voltage from photoresistor
	voltage = 0
	for i in range(10):
		voltage += GPIO.input(photo_pin)
	voltage /= 10
	#convert voltage to a light intensity value
	max_voltage = 5 #max voltage output of Raspberry Pi
	max_intensity = 3500 # max light intensity value
	light_intensity = voltage * max_intensity / max_voltage
	
	return light_intensity

def get_light():
	#Continuously measure sunlight intensity and length of intensity
	sunlight_on = False
	sunlight_start_time = time.time()
	while True:
		intensity = get_light_intensity()
		if intensity > sunlight_threshold and not sunlight_on:
			sunlight_on = True
			sunlight_start_time = time.time()
			print("sunlight on")
		elif intensity <= sunlight_threshold and sunlight_on:
			sunlight_on = False
			sunlight_duration = time.time() - sunlight_start_time
			print("sunlight off, duration: {:.2f} seconds".format(sunlight_duration))
			print("Intensity: {:.2f}".format(intensity))
		time.sleep(1)		

