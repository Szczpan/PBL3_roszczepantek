import RPi.GPIO as GPIO
import serial
from time import time, sleep
import sys

uart = serial.Serial("/dev/ttyS0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=8, timeout=1)

sreadlen = 1024 # max number of chars to read from serial in one try 

#GET DATA FROM UART
def readData():
    received_data = ''
    while uart.inWaiting():
        received_data += (uart.read(uart.inWaiting())).decode('utf-8')
        sleep(0.5)
    return received_data

#SEND AT COMMANDS
def sendAT(command):
    if not uart.inWaiting():
        uart.write((command + '\r\n').encode('utf-8'))
        sleep(0.5)
        return readData()
    return 0

#SEND DATA IN HEX FORMAT
def send_data_hex(hex_data):
    msg = f'{hex_data}'
    uart.write((f'AT+TEST=TXLRPKT, "{msg}"'))
    
#TEST CONNECTION WITH LORA E5 MODULE
def connectTest():
    response = sendAT('AT')
    print(f'Lora E5 connection status: {response}')
    return response
    
#CONFIG FUNCTION FOR MODULE
def loraConf():
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

NODE_ID = 9

if __name__ == "__main__":
    if loraConf() == 0:
        print("Error occured: connecting error")
        exit()
    hex_nodeID = hex(NODE_ID).lstrip("0x").zfill(4)
    hex_temperatureMeas = '0A'
    hex_moisureMeas = '0B'
    msg=f'{hex_nodeID}{hex_temperatureMeas}{hex_moisureMeas}'
    send_data_hex()
    
    
    