# / usr / bin / python3
# soil moisture .py
import spidev
import time
max = 460.0 # Maximum value at full humidity
spi = spidev.SpiDev()
spi.open(0, 1)
answer = spi.xfer([1, 128, 0])
def run_circuit():
	if 0 <= answer[1] <= 3:
		value = 1023 - ((answer [1] * 256) + answer [2])
		percentage_value = ((value / max) *100)
		print("Soil moisture:", percentage_value, "%")
		#time.sleep(2.0)
	else:
		print(f"Moisture magnitude is {answer[1]}")
		#time.sleep(2.0)
run_circuit()
