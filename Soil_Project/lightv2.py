import RPi.GPIO as GPIO
import time
# import matplotlib.pyplot as plt

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

try:
	while True:
		print(rc_time(pin_to_circuit))
	while False:
		print("Error")
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()
