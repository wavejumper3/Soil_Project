import humidityv3
from lightv5 import get_light
import moisturev3

for x in range(2):

	humidityv3.humidity()
	get_light()
	moisturev3.run_circuit()
	#time.sleep(2.0)
