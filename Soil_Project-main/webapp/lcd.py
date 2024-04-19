import RPi.GPIO as GPIO
import spidev
import time
import board
import Adafruit_DHT
import psutil
import spidev
from flask import Flask, render_template
from RPLCD import CharLCD
app = Flask(__name__)
#spi = spidev.SpiDev()

#setting up pins on pi
GPIO.setmode(GPIO.BCM)
#Humidity setup
DHT_PIN = 23
GPIO.setup(DHT_PIN, GPIO.OUT)
# check and terminate any running libgpiod process.

lcd = CharLCD(i2c_expander='PCF8574', address=0x3F, port=1, cols=16, rows=2)

def humidity():
        try:
                humidity, temp = Adafruit_DHT.read(Adafruit_DHT.DHT11, 23)
                return temp, humidity
		lcd.cursor_pos(0,0)
               	lcd.write_string("Temperature: {}*C".format(temp))
		lcd.cursor_pos(1,0)
		lcd.write_string("Humidity: {}%".format(humidity))
		# print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
        except RuntimeError as error:
                print(error.args[0])

humidity()
