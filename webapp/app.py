import RPi.GPIO as GPIO
import time
import board
import Adafruit_DHT
import psutil
import spidev
from flask import Flask, render_template
app = Flask(__name__)

#setting up pins on pi
GPIO.setmode(GPIO.BCM)

#Light program setup
photo_pin = 17
GPIO.setup(photo_pin, GPIO.IN)
#Set the threshold value for sunlight detection
sunlight_threshold = 500
intensity_history = [] #store intensity values
def get_light_intensity():
	GPIO.setmode(GPIO.BCM)	
	GPIO.setup(photo_pin, GPIO.IN)
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
	# puts timeout at 1 second - will only measure light for 1 second
	timeout = time.time() + 5
	intensity = 0 # initalizes intensity variable
	while True:
		new_intensity = get_light_intensity()
		
		if new_intensity > sunlight_threshold and not sunlight_on:
			sunlight_on = True
			sunlight_start_time = time.time()
			print("sunlight on")
		elif new_intensity <= sunlight_threshold and sunlight_on:
			sunlight_on = False
			sunlight_duration = time.time() - sunlight_start_time
			print("sunlight off, duration: {:.2f} seconds".format(sunlight_duration))
		if time.time() > timeout:
			break
		
	#Update new instensity
	intensity = new_intensity

	time.sleep(1)		
	return intensity


#Moisture setup
max = 460.0 # Maximum value at full humidity
spi = spidev.SpiDev()
spi.open(0, 1)
answer = spi.xfer([1, 128, 0])
def run_circuit():
	GPIO.setmode(GPIO.BCM)
	moisture = 0
	if 0 <= answer[1] <= 3:
		value = 1023 - ((answer [1] * 256) + answer [2])
		percentage_value = ((value / max) *100)
		moisture = percentage_value
		print("Soil moisture:", percentage_value, "%")
		#time.sleep(2.0)
	else:
		moisture = percentage_value
		print(f"Moisture magnitude is {answer[1]}")
		#time.sleep(2.0)
	return moisture
#run_circuit()


#Humidity setup
DHT_PIN = 23
GPIO.setup(DHT_PIN, GPIO.OUT)
# check and terminate any running libgpiod process.

def humidity():
	try:
		humidity, temp = Adafruit_DHT.read(Adafruit_DHT.DHT11, 23)
		return temp, humidity
		print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
	except RuntimeError as error:
		print(error.args[0])
		#time.sleep(2.0)
	
#humidity()

#Route to different pages on website 
# '/' is main route - when you load page this is what will happen first
@app.route('/')
def index():
	
	templateData = {
		'title': 'SJU Community Garden Data',
		'Temperature': humidity(),
		'Light': get_light(),
		'Soil_Moisture': run_circuit()
	
	}
	return render_template('index.html', **templateData)

@app.route('/hello/pi2')
def hello():
	return render_template('page.html')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')


