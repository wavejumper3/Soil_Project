import RPi.GPIO as GPIO
import spidev
import time
import board
import Adafruit_DHT
import psutil
import spidev
import sqlite3
from datetime import datetime
from flask import Flask, render_template
import pandas as pd
app = Flask(__name__)
#spi = spidev.SpiDev()

#setting up pins on pi
GPIO.setmode(GPIO.BCM)

#Light program setup
photo_pin = 17
GPIO.setup(photo_pin, GPIO.IN)
'''
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
'''
def light_on():
	# If light on sensor, return Yes else return No
	if GPIO.input(photo_pin) > 0:
		return "Yes"
	else:
		return "No"
'''
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
'''
# Inputs sensor values to SQL DB
def insert_sensor_data(temperature, humidity, soil_moisture, light_sensor):
    conn = sqlite3.connect('/home/pi/Desktop/Soil_Project-main/community_garden.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%D %I:%M:%S-%p")
    #Insert sensor data into the table
    c.execute('''INSERT INTO garden_data(date, temp, humid, soil, light_duration) VALUES(?,?,?,?,?)''', (timestamp, temperature, humidity, soil_moisture, light_sensor))
    conn.commit()

#Moisture setup
channel = 7
def moisture_detect():
    print("Moisture method being called")
    '''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN)

    def callback(channel):
        if GPIO.input(channel):
            print("no water detected")
        else:
            print("water detected")
            
    GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300) # let us know when the pen goes HIGH or LOW
    GPIO.add_event_callback(channel, callback) # assign function to GPIO PIN, Run function on change
    time.sleep(10)
    '''

#Humidity setup
DHT_PIN = 23
GPIO.setup(DHT_PIN, GPIO.OUT)
# check and terminate any running libgpiod process.

def humidity():
	try:
		humidity, temp = Adafruit_DHT.read(Adafruit_DHT.DHT11, 24)
		insert_sensor_data(temp, humidity, 50, light_on())
		print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
		return temp, humidity
	except RuntimeError as error:
		print(error.args[0])
		#time.sleep(2.0)
	
#humidity()

#Route to different pages on website 
# '/' is main route - when you load page this is what will happen first
#@app.route('/')
#def index():
	
#	templateData = {
#		'title': 'SJU Community Garden Data',
#		'Temperature': humidity(),
#		'Light': get_light(),
#		'Soil_Moisture': moisture_detect()
#	
#	}
#	return render_template('index.html', **templateData)


@app.route('/export_excel')
def export_excel():
    # Connect to SQLite database
	conn = sqlite3.connect('/home/pi/Desktop/Soil_Project-main/community_garden.db')

    # Query data from database
	query = 'SELECT * FROM garden_data'
   	df = pd.read_sql_query(query, conn)
    # Export data to Excel
	excel_file = 'garden_data.xlsx'
	df.to_excel(excel_file, index=False)

    # Close database connection
	conn.close()

    # Return Excel file as response
	return send_file(excel_file, as_attachment=True)

@app.route('/')
def data():
	humidity()
	# Connect to the SQLite database
    	conn = sqlite3.connect('/home/pi/Desktop/Soil_Project-main/community_garden.db')
   	c = conn.cursor()
   	# Query data from the database
   	c.execute('SELECT date, temp, humid, soil, light_duration FROM garden_data')
   	data = c.fetchall()
   	# Close the database connection
   	conn.close()
   	# Render the HTML template with the data
   	return render_template('data.html', data=data)

@app.route('/hello/pi2')
def hello():
	return render_template('page.html')
@app.route('/new-gui')
def newgui():
	templateData = {
		'Temperature': humidity(),
		'Light': get_light(),
		'Soil_Moisture': moisture_detect()
	}
	return render_template('index.html', **templateData)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')



