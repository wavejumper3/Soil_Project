import RPi.GPIO as GPIO
import time
import board
import analogio

# import matplotlib.pyplot as plt

readPIN = 17
photo_pin = analogio.AnalogIn(board.A0)
resistor = 10000

def calc_light_intensity(analog_val, resistor):
	voltage = analog_val * 3.3 / 65536
	lux = (2500 / voltage - 500) / resistor
	return lux
	
	


def rc_time(readPin):

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(readPIN,GPIO.IN)
	GPIO.setwarnings(True)
	
	try:
	 while True:
	  analog_value = photo_pin.value
	  light_intensity = calc_light_intensity(analog_value, resistor)
	  print("Light intensity: {:.2f} lux".format(light_intensity)
	  #time.sleep(1)
	  
	  '''
	  print (" Read: " + str(GPIO.input(readPIN)) + " ", end='\r')
	  time.sleep(1)
	  '''
	except KeyboardInterrupt:
	  print('interrupted!')
	  GPIO.cleanup()



'''
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin_to_circuit = 11
initial_time = 0

from spidev import SpiDev
 
class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000 # 1MHz
 
    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz
    
    def read(self, channel = 0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
            
    def close(self):
        self.spi.close()

def rc_time(pin_to_circuit):
	count = 0
	GPIO.setup(pin_to_circuit, GPIO.OUT)
	GPIO.output(pin_to_circuit, GPIO.LOW)
	#cltime.sleep(2.0)

	GPIO.setup(pin_to_circuit, GPIO.IN)

	while (GPIO.input(pin_to_circuit) == GPIO.LOW):
		count += 1

	return (count)

try:
	while True:
		print(rc_time(pin_to_circuit))
		break
	while False:
		print("Error")

except KeyboardInterrupt:
	pass
#finally:
	#GPIO.cleanup()
	
'''
