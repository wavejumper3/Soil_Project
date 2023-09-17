import humidityv3
from lightv5 import get_light
from moisturev3 import run_circuit
import datetime
import subprocess
import signal
import time

start_time = time.time()
time_limit = 10

def timeout_handler(signum, frame):
	raise TimeoutError('Timeout expired')
	
timeout = 5

data = "Data: \n"
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(timeout)

try:
	data += str( humidityv3.humidity() )
	#data += "\n" + str( get_light() )
	data += "\n" + str( run_circuit() )
	data += "\n" + "Time recorded: " + str( datetime.datetime.now() )
	subprocess.run(['python', 'Gardenv2.py', '>', 'output.txt'])
	time.sleep(60)
	pass
except TimeoutError:
	print("The operation timed out")
finally:
	signal.alarm(0)
	
with open("output.txt", "w") as f:
	f.write( str(data) )
