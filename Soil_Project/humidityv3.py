import time
import board
import adafruit_dht
import psutil
# check and terminate any running libgpiod process.
def humidity():
	for proc in psutil.process_iter():
		if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
			proc.kill()
	sensor = adafruit_dht.DHT11(board.D23)

	try:
		temp = sensor.temperature
		humidity = sensor.humidity
		print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
	except RuntimeError as error:
		print(error.args[0])
		#time.sleep(2.0)
	
	except Exception as error:
		sensor.exit()
		raise error
		
humidity()
