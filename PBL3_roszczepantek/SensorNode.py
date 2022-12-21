import RPi.GPIO as GPIO
import serial
from time import time, sleep
import sys

uart = serial.Serial("/dev/ttyS0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=8, timeout=1)

sreadlen = 1024 # max number of chars to read from serial in one try 

#SEND AT COMMANDS
def sendAT(command):
    if not uart.inWaiting():
        uart.write((command + '\r\n').encode('utf-8'))
        sleep(0.5)
        return readData()
    return 0

def send_data_hex(nodeID, data):
    msg = f'{nodeID}{hex(data)}'
    uart.write((f'AT+TEST=TXLRPKT, "{msg}"'))
    
#CONFIG FUNCTION FOR MODULE
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

if __name__ == "__main__":
    if loraConf("00 01 0F 2C", 8) == 0:
        print("Error occured: connecting error")
        exit()
    
    