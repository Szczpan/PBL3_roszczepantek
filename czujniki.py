import RPi.GPIO as GPIO
import dht11
import time
import datetime

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)

# read data using pin 37 (GPIO26)
instance = dht11.DHT11(pin=26)

try:
	while True:
		result = instance.read()
		moisure=GPIO.input(16)
		#if result.is_valid():
		print("Last valid input: " + str(datetime.datetime.now()))
		print("Temperature: %-3.1f C" % result.temperature)
		print("Humidity: %-3.1f %%" % result.humidity)
		print("Moisure: %-3.1f %%" % moisure)
		time.sleep(6)
except KeyboardInterrupt:
	print("Cleanup")
	GPIO.cleanup()
