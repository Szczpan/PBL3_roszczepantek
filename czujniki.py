import RPi.GPIO as GPIO
import dht11
import time
import os
import datetime
import subprocess
import sys

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
		wateringMin=250+100*(result.temperature-15)/6
		os.system("cat /sys/bus/iio/devices/iio\:device0/in_voltage0-voltage1_raw")
		moistureRaw=subprocess.Popen([sys.executable, 'home/pi/Documents/Project/Subprocess/Beep2.py'], shell = True)
		print(moistureRaw)
		moisture=float(moistureRaw)*0.1875/3.3*100
		print(moisture)
		#if result.is_valid():
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
