import RPi.GPIO as GPIO
import dht11
from subprocess import Popen, PIPE
from shlex import split
from operations import SensorNode

HIGH = 1
LOW = 0

def sensor_meas(dht_11_pin, moist_sensor_pin):
 	# read data from DHT 11 sensor
	dht_11_meas = read_DHT_11(dht_11_meas)

	# read data from DFRobot Moisture Sensor v2
	moist_meas = read_moisture(moist_sensor_pin)
	
	# saves data to SensorNode object
	measure = SensorNode(None, dht_11_meas.humidity, moist_meas, dht_11_meas.temperature, None)
	
	# prints saved data
	measure.print_data()
 	
	return(measure)


# reads data from DFRobot Moisture V2 Sensor
def read_moisture(pin):
    process = Popen(split("cat /sys/bus/iio/devices/iio\:device0/in_voltage0-voltage1_raw"), stdout = PIPE)
    moistureRaw = process.stdout.readline()
    moisture = float(moistureRaw) / 17670 * 100
    return moisture


# reads data from DHT 11 sensor
def read_DHT_11(dht_pin):
	instance = dht11.DHT11(dht_pin)
	
	for i in range(20):
		result = instance.read()
		if result.is_valid():
			return result

	return None


# Calculates need for water (returns True / False)
# def water_need_calc(measure):
# 	wateringMin=10
#     wateringMin = max(25, 25 + 10 * (measure.temperature - 15) / 6)
    

# Controls valve    
def control_valve(valve_pin, state):
	if state == True: 
		GPIO.output(valve_pin, HIGH)
		return True

	if state == False: 
		GPIO.output(valve_pin, LOW)
		return False

	return None
