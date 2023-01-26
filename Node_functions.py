from operations import SensorNode, ValveNode, Nodes
from time import time, sleep
from rpi_server_comm import update_sensor, update_valve
from get_weather import get_rain_sum
from random import randrange
import RPi.GPIO as GPIO
import serial
import sys
import os
import requests
import json
import re
import dht11
from subprocess import Popen, PIPE
from shlex import split


HIGH = 1
LOW = 0

VALVE_ID = 1
SENSOR_ID = 9
MAIN_ID = 10

VALVE_PIN = 23
DHT11_SENSOR_PIN = 26
MOIST_SENSOR_PIN = 16

SENSOR_SEND_PACKETS = 10


###    UART COMMUNICATION    ####

# Setup for UART
uart = serial.Serial("/dev/ttyS0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=8, timeout=1)


# Sends AT commands with UART and returns received answers
def sendAT(command):
    if not uart.inWaiting():
        uart.write((command + '\r\n').encode('utf-8'))
        sleep(0.5)
        return readData()
    return 0


# Reads data from UART
def readData():
    received_data = ''
    while uart.inWaiting():
        received_data += (uart.read(uart.inWaiting())).decode('utf-8')
        sleep(0.1)
    return received_data



###    LORA MODULE    ###    

# Sends LoRa message in hex
def send_data_hex(hex_data):
    sendAT(f'AT+TEST=TXLRPKT, "{hex_data}"')
   

# Capture data from LoRa
def receiveData():
    sendAT('AT+TEST=RXLRPKT')
    sleep(5)
    return readData()


# Tests connection with LoRa module
def connectTest():
    response = sendAT('AT')
    print(f'Lora E5 connection status: {response}')
    return response


# Config for LoRa mdoule
def loraConf():
    readData()
    if not ('+AT: OK\r\n' in connectTest()):
        return 0
    last_response = sendAT('AT+RESET')
    sleep(0.5)
    print(f'Reseting LoRa module to default: {last_response}')
    sleep(0.5)
    while last_response != '+MODE: TEST\r\n':
        sendAT('AT+MODE=TEST')
        last_response = sendAT('AT+MODE')
        sleep(0.1)
        print(f'Changing LoRa module mode to TEST: {last_response}')
    return 1



###    DATA PROCESSING    ###

# Gets random data from sensors
def getSensorData_random():
    sensor = SensorNode(None, None, None, None, None)
    sensor.air_temperature = randrange(0, 255, 1)
    sensor.air_humidity = randrange(0, 255, 1)
    sensor.soil_moisture = randrange(0, 255, 1)
    sensor.battery_level = randrange(0, 255, 1)
    
    return sensor


# Gets data from sensors
def getSensorData(dht_11_pin, moist_sensor_pin):
    # reads data from DHT 11 sensor
    dht_11_meas = read_DHT_11(dht_11_pin)
    if dht_11_meas is None: return None

    # reads data from DFRobot Moisture Sensor v2
    moist_meas = read_moisture(moist_sensor_pin)
    if moist_meas is None: return None
    
    # reads battery level data
    battery_meas = read_battery_lev()
    if battery_meas is None: return None
    
    # saves data to SensorNode object
    sensor = SensorNode(None, dht_11_meas.humidity, moist_meas, dht_11_meas.temperature, None)

    # prints saved data
    sensor.print_data()

    return(sensor)


# Reads battery level
def read_battery_lev():
    return randrange(95, 100, 0.1)


# Reads data from DFRobot Moisture V2 Sensor
def read_moisture(pin):
    process = Popen(split("cat /sys/bus/iio/devices/iio\:device0/in_voltage0-voltage1_raw"), stdout = PIPE)
    moistureRaw = process.stdout.readline()
    moisture = float(moistureRaw) / 17670 * 100
    return moisture


# Reads data from DHT 11 sensor
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


# Processes data from sensor node
def sensorDataProcess (msg):
    # msg_index = RAW_msg.find('"') + 1
    sensor = SensorNode(None, None, None, None, None)
    sensor.sensor_id = int(f'0x{msg[0]}{msg[1]}{msg[2]}{msg[3]}', 16)
    sensor.air_humidity = int(f'0x{msg[4]}{msg[5]}', 16)
    sensor.soil_moisture = int(f'0x{msg[6]}{msg[7]}', 16)
    sensor.air_temperature = int(f'0x{msg[8]}{msg[9]}', 16)
    sensor.battery_level = int(f'0x{msg[10]}{msg[11]}', 16)
    return sensor


# Processes valve data
def valveDataProcess (msg):
    valve = ValveNode(None, None, None)
    valve.valve_id = int(f'0x{msg[0]}{msg[1]}{msg[2]}{msg[3]}', 16)
    valve.is_open = int(f'0x{msg[4]}{msg[5]}', 16)
    valve.time_left = int(f'0x{msg[6]}{msg[7]}', 16)
    return valve    


# Captures data from sensor node and uploads it to its class
def getLoRaSensor(RAW_msg):
    #message = receiveData()
    if RAW_msg != ' ' and RAW_msg != '':
        print(f'Odebrane dane: \n{RAW_msg}')
        sensor = sensorDataProcess(RAW_msg)
        return sensor
    return 0

def getLoRaValve(RAW_msg):
    if RAW_msg != ' ' and RAW_msg != '':
        print(f'Odebrane dane: \n{RAW_msg}')
        valve = valveDataProcess(RAW_msg)
        return valve
    return 0


# Captures LoRa data from choosen nodes and saves it to choosen mode (0 - sensor class; 1 - valve class, 2 - both)
def getLora(list_of_sensor_nodes, list_of_valve_nodes):
    RAW_msg = receiveData()
    list_of_nodes = list_of_sensor_nodes + list_of_valve_nodes
    nodes = Nodes()
    nodes.SensorNode = None
    nodes.ValveNode = None
    # print(f'Lista czujnikow: {list_of_sensor_nodes}')
    # print(f'Lista zaworow: {list_of_valve_nodes}')
    # print(f'Wybrany tryb to: {mode}')

    if RAW_msg != ' ' and RAW_msg != '':
        node_list = checkNodeID(RAW_msg)
        # print(f"Sprawdzanie czy node {node_id} jest na liscie {list_of_nodes}")
        for node in node_list:
            node_id = int("0x" + node[:4], 16)
            if node_id in list_of_nodes:
                if node_id in list_of_sensor_nodes:
                    # nodes.ValveNode = getLora(VALVE_MODE, [], list_of_valve_nodes)
                    print(f'Odebrane dane: \n{node}')
                    nodes.SensorNode = sensorDataProcess(node)
                elif node_id in list_of_valve_nodes:
                    print(f'Odebrane dane: \n{node}')
                    nodes.ValveNode = valveDataProcess(node)
        return nodes
    return None


def checkNodeID(RAW_msg):
    # msg_index = RAW_msg.find('"') + 1
    # msg = RAW_msg[msg_index:]
    # node_id = int(f'0x{msg[0]}{msg[1]}{msg[2]}{msg[3]}', 16)
    node_list = re.findall('RX "(.*)"', RAW_msg)
    return node_list



###    SERVER COMMUNICATION    ###
SERVER_IP = "http://10.140.123.3:8000/api-v1/devices"

def create_sensor_list(node_id):
    data = requests.get(SERVER_IP)
    data = json.loads(data.text)
    sensor_list = []
    for device in data["devices"]:
        if node_id == device["main-id"]:
            for sensor in device["sensor-nodes"]:
                sensor_list.append(sensor["sensor-id"])
    
    return sensor_list


def create_valve_list(node_id):
    data = requests.get(SERVER_IP)
    data = json.loads(data.text)
    valve_list = []
    for device in data["devices"]:
        if node_id == device["main-id"]:
            for valve in device["valve-nodes"]:
                valve_list.append((valve["valve-id"]))

    return valve_list


def get_sensor_soil(node_id):
    data = requests.get(SERVER_IP)
    data = json.loads(data.text)
    soil_list = []
    for device in data["devices"]:
        if node_id == device["main-id"]:
            for sensor in device["sensor-nodes"]:
                soil_list.append(sensor["soil-moisture"])
    if len(soil_list) == 0:
        return 0

    moisture_sum = 0
    moisture_n = 0
    for moisture in soil_list:
        if moisture >= 0:
            moisture_sum += moisture
            moisture_n += 1

    if moisture_n == 0:
        return 0

    return moisture_sum/moisture_n
