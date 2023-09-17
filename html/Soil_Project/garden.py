import time
import board
import RPi.GPIO as GPIO
import adafruit_dht
import psutil
import spidev

#-----------------Light---------------------
GPIO.setmode(GPIO.BOARD)

pin_to_circuit = 11
initial_time = 0

def rc_time(pin_to_circuit):
	count = 0
	GPIO.setup(pin_to_circuit, GPIO.OUT)
	GPIO.output(pin_to_circuit, GPIO.LOW)
	time.sleep(2.0)

	GPIO.setup(pin_to_circuit, GPIO.IN)

	while (GPIO.input(pin_to_circuit) == GPIO.LOW):
		count += 1

	return (count)

#-----------------Humidity---------------------
# check and terminate any running libgpiod process.
for proc in psutil.process_iter():
	if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
		proc.kill()
sensor = adafruit_dht.DHT11(board.D23)


#-----------------Moisture---------------------
max = 460.0 # Maximum value at full humidity
spi = spidev.SpiDev()
spi.open(0, 1)
answer = spi.xfer([1, 128, 0])



def run_circuit():
	#Moisture-------------------------------------------
	if 0 <= answer[1] <= 3:
		value = 1023 - ((answer [1] * 256) + answer [2])
		percentage_value = ((value / max) *100)
		print("Soil moisture:", percentage_value, "%")
		time.sleep(2.0)
	else:
		print(f"Moisture magnitude is {answer[1]}")
		time.sleep(2.0)
		
	#Humidity-------------------------------------------------------------
	try:
		temp = sensor.temperature
		humidity = sensor.humidity
		print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
	except RuntimeError as error:
		print(error.args[0])
		time.sleep(2.0)
	except Exception as error:
		sensor.exit()
		raise error
	time.sleep(2.0)
	
	#Light----------------------------
	try:
		while True:
			print(rc_time(pin_to_circuit))
		while False:
			print("Error")
	except KeyboardInterrupt:
		pass
	finally:
		GPIO.cleanup()
	
	run_circuit()
run_circuit()
