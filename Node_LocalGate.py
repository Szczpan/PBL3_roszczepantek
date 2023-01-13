import RPi.GPIO as GPIO
import serial
from time import time, sleep
import sys
from operations import SensorNode, ValveNode
from rpi_server_comm import update_sensor, update_valve
import requests
import json
from get_weather import get_rain_sum


uart = serial.Serial("/dev/ttyS0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=8, timeout=1)

sreadlen = 1024 # max number of chars to read from serial in one try 

#GET DATA FROM UART
def readData():
    received_data = ''
    while uart.inWaiting():
        received_data += (uart.read(uart.inWaiting())).decode('utf-8')
        sleep(0.5)
    return received_data

#TEST CONNECTION WITH LORA E5 MODULE
def connectTest():
    response = sendAT('AT')
    print(f'Lora E5 connection status: {response}')
    return response

#SEND AT COMMANDS
def sendAT(command):
    if not uart.inWaiting():
        uart.write((command + '\r\n').encode('utf-8'))
        sleep(0.5)
        return readData()
    return 0

#SEND DATA IN HEX FORMAT
def send_data_hex(hex_data):
    sendAT(f'AT+TEST=TXLRPKT, "{hex_data}"')


#CAPTURE DATA
def receiveData():
    sendAT('AT+TEST=RXLRPKT')
    sleep(0.5)
    return readData()


#CONFIG FUNCTION FOR MODULE
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


#PROCESS DATA FROM SENSOR NODE
def sensorDataProcess (RAW_msg):
    msg_index = RAW_msg.find('"') + 1
    msg = RAW_msg[msg_index:]
    #print(f'wiadomosc: {msg}')
    s_nodeID = f'0x{msg[0]}{msg[1]}{msg[2]}{msg[3]}'
    s_temperature_meas = f'0x{msg[4]}{msg[5]}'
    s_moisture_meas = f'0x{msg[6]}{msg[7]}'
    nodeID = int(s_nodeID,16)
    temperature_meas = int(s_temperature_meas,16)
    moisture_meas = int(s_moisture_meas,16)
    processed_data = [nodeID, temperature_meas, moisture_meas]
    return processed_data
    

#GET DATA FROM SENSOR NODE AND UPLOAD TO ITS CLASS
def get_lora_sensor():
    last_response = receiveData()
    if last_response != ' ' and last_response != '':
        print(f'Odebrane dane: \n{last_response}')
        sensor_data = sensorDataProcess(last_response)
        sensor = SensorNode(sensor_data[0], 0, sensor_data[2], sensor_data[1], 0)
        return sensor
    return 0


#OPENS VALVE FOR CERTAIN TIME (for time = -1 closes it)
def open_valve(nodeID, time):
    return 1


MY_ID = 10
SERVER_IP = "http://10.140.123.3:8000/api-v1/devices"


def create_sensor_list():
    data = requests.get(SERVER_IP)
    data = json.loads(data.text)
    sensor_list = []
    for device in data["devices"]:
        if MY_ID == device["main-id"]:
            for sensor in device["sensor-nodes"]:
                sensor_list.append(sensor["sensor-id"])
    
    return sensor_list


def create_valve_list():
    data = requests.get(SERVER_IP)
    data = json.loads(data.text)
    valve_list = []
    for device in data["devices"]:
        if MY_ID == device["main-id"]:
            for valve in device["valve-nodes"]:
                valve_list.append((valve["valve-id"]))

    return valve_list


def get_sensor_soil():
    data = requests.get(SERVER_IP)
    data = json.loads(data.text)
    soil_list = []
    for device in data["devices"]:
        if MY_ID == device["main-id"]:
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


if __name__ == "__main__":
    if loraConf() == 0:
        print("Error occured: connecting error")
        exit()
    last_time = time()
    while True:
        sensor_id_list = create_sensor_list()

        # if have something to send check if sensor id is in sensors attached to me
        sensor = get_lora_sensor()

        time_left = 0
        # print in terminal
        if sensor != 0:
            print(f'node id: {sensor.sensor_id}')
            print(f'wilgotnosc: {sensor.soil_moisture}')
            print(f'temperatura: {sensor.air_temperature}')
            print('\n')

            if sensor.sensor_id in sensor_id_list:
                update_sensor(MY_ID, sensor)
        
        forecast_rain = get_rain_sum()
        soil_avg = get_sensor_soil()
        valve_list = create_valve_list()

        if sensor != 0:
            if soil_avg*forecast_rain < 200:
                for valve in valve_list:
                    valve_obj = ValveNode(valve, True, 100)
                    time_left = 100
                    update_valve(MY_ID, valve_obj)
            else:
                for valve in valve_list:
                    valve_obj = ValveNode(valve, False, 0)
                    time_left = 0
                    update_valve(MY_ID, valve_obj)
            last_time = time()
        else:
            for valve in valve_list:
                time_left -= time() - last_time
                if time_left > 0:
                    valve_obj = ValveNode(valve, True, time_left)
                    update_valve(MY_ID, valve_obj)
                else:
                    valve_obj = ValveNode(valve, False, 0)
                    time_left = 0
                    update_valve(MY_ID, valve_obj)
                
        sleep(0.5)
        