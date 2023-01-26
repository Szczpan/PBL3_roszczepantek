import RPi.GPIO as GPIO
import dht11
import time
import os
import datetime
import subprocess
import sys
import shlex
import re



def meas():
	# initialize GPIO
	GPIO.setwarnings(True)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(26, GPIO.IN)
	GPIO.setup(16, GPIO.IN)
	GPIO.setup(23, GPIO.OUT)

	wateringMin=10

	# read data using pin 37 (GPIO26)
	instance = dht11.DHT11(pin=26)

	try:
		while True:
			result = instance.read()
			wateringMin=min(25, 25+10*(result.temperature-15)/6)
			#os.system("cat /sys/bus/iio/devices/iio\:device0/in_voltage0-voltage1_raw")
			process = subprocess.Popen(shlex.split("cat /sys/bus/iio/devices/iio\:device0/in_voltage0-voltage1_raw"), stdout=subprocess.PIPE)
			moistureRaw=process.stdout.readline()
			#print(moistureRaw)
			# moistureRaw = re.findall("b'(\d*)\\n'", str(moistureRaw, "utf-8"))
			# moistureRaw=moistureRaw[2:-2]
			# print(moistureRaw)
			moisture=float(moistureRaw)/17670*100
			#print(moisture)
			if result.is_valid():
				print("Last valid input: " + str(datetime.datetime.now()))
				print("Temperature: %-3.1f C" % result.temperature)
				print("Humidity: %-3.1f %%" % result.humidity)
				print("Moisture: %-3.1f %%" % moisture)
				time.sleep(6)
				if moisture < wateringMin:
					GPIO.output(23,1)
					print("podlewam")
					time.sleep(4)
					GPIO.output(23,0)


	except KeyboardInterrupt:
			print("Cleanup")
