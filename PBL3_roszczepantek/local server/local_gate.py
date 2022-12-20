import RPi.GPIO as GPIO
import serial
from time import time, sleep
import sys

uart = serial.Serial("/dev/ttyS0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=8, timeout=1)

sreadlen = 1024 # max number of chars to read from serial in one try 

def readData():
    received_data = ''
    while uart.inWaiting():
        received_data += (uart.read(uart.inWaiting())).decode('utf-8')
        sleep(0.5)
    return received_data

def connectTest():
    response = sendAT('AT')
    print(f'Lora E5 connection status: {response}')
    return response

def sendAT(command):
    if not uart.inWaiting():
        uart.write((command + '\r\n').encode('utf-8'))
        sleep(0.5)
        return readData()
    return 0

def send_data_hex(nodeID, data):
    msg = f'{nodeID}{hex(data)}'
    uart.write((f'AT+TEST=TXLRPKT, "{msg}"'))
    
def receiveData():
    sendAT('AT+TEST=RXLRPKT')
    return readData()

def loraConf(id, port):
    if connectTest() != '+AT: OK\r\n': 
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

def dataProcess (msg):
    s_nodeID = [f'0x{msg[0]}{msg[1]}{msg[2]}{msg[3]}']
    s_temperature_meas = f'0x{msg[4]}{msg[5]}'
    s_moisture_meas = f'0x{msg[6]}{msg[7]}'
    print(s_nodeID, s_temperature_meas, s_moisture_meas)
    h_nodeID = [int(s_nodeID[0], 16), int(s_nodeID[1], 16)]
    h_temperature_meas = int(s_temperature_meas,16)
    h_moisture_meas = int(s_moisture_meas,16)
    print(h_nodeID, h_temperature_meas, h_moisture_meas)
    #nodeID = [int(x,base=16)]
    #temperature_meas = [int(x,base=16) for x in h_temperature_meas]
    #moisture_meas = [int(x,base=16) for x in h_moisture_meas]
    
    #processed_data = [nodeID, temperature_meas, moisture_meas]
    #return processed_data
    
        
    

def main():
    sensor_data = dataProcess('50F60F0A')
    print(sensor_data)
    while True:
        last_response = receiveData()
        if last_response != ' ':
            break
    
    
    
    



if __name__ == "__main__":
    if loraConf("00 01 0F 2C", 8) == 0:
        print("Error occured: connecting error")
        exit()
    while True:
        main()