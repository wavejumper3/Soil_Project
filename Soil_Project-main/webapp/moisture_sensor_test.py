import RPi.GPIO as GPIO
import time

# Set GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Define GPIO pin for the moisture sensor
moisture_sensor_pin = 15 

# Setup GPIO pin as input
GPIO.setup(moisture_sensor_pin, GPIO.IN)

def read_moisture_level():
    # Read the digital value from the sensor
    moisture_level = GPIO.input(moisture_sensor_pin)
    return moisture_level

try:
    while True:
        # Read moisture level
        moisture_value = GPIO.input(moisture_sensor_pin)

        # Print the moisture level
        print("Moisture Level: {}".format(moisture_value))

        # Add a delay before reading again (adjust as needed)
        time.sleep(1)

except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    GPIO.cleanup()

