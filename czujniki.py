import RPi.GPIO as GPIO
import dht11
import time
import os
import datetime
<<<<<<< HEAD
from operations import SensorNode
=======
import subprocess
import sys
import shlex
import re
>>>>>>> d316210d7d0f027dbdcde123ea88041f1b602a59

def meas():
	# initialize GPIO
	GPIO.setwarnings(True)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(26, GPIO.IN)
	GPIO.setup(16, GPIO.IN)
	GPIO.setup(23, GPIO.OUT)

	wateringMin=10
	temp=1

	# read data using pin 37 (GPIO26)
	instance = dht11.DHT11(pin=26)

	try:
		while temp:
			result = instance.read()
			wateringMin=min(25, 25+10*(result.temperature-15)/6)
			process = subprocess.Popen(shlex.split("cat /sys/bus/iio/devices/iio\:device0/in_voltage0-voltage1_raw"), stdout=subprocess.PIPE)
			moistureRaw=process.stdout.readline()
			moisture=float(moistureRaw)/17670*100
			if result.is_valid():
				print("Last valid input: " + str(datetime.datetime.now()))
				print("Temperature: %-3.1f C" % result.temperature)
				print("Humidity: %-3.1f %%" % result.humidity)
				print("Moisture: %-3.1f %%" % moisture)
				# time.sleep(6)
				temp=0
				# if moisture < wateringMin:
				# 	GPIO.output(23,1)
				# 	print("podlewam")
				# 	time.sleep(4)
				# 	GPIO.output(23,0)


	except KeyboardInterrupt:
			print("Cleanup")

meas()
