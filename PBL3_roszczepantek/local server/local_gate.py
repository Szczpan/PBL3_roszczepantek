import RPi.GPIO as GPIO
import serial
from time import time, sleep
import sys

uart = serial.Serial("/dev/ttyS0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=8, timeout=1)

sreadlen = 1024 # max number of chars to read from serial in one try 

def readData():
    received_data = ''
    if uart.inWaiting():
        received_data += (uart.read(uart.inWaiting())).decode('utf-8')
        sleep(0.5)
        print(received_data)
    return received_data

def connectTest():
    uart.write(('AT').encode('utf-8'))
    return readData()

def sendAT(command):
    uart.write((f'{command}').encode('utf-8'))
    sleep(0.5)
    return readData()

def send_data_hex(nodeID, data):
    msg = f'{nodeID}{hex(data)}'
    uart.write((f'AT+TEST=TXLRPKT, "{msg}"'))
    
def receiveData():
    sendAT('AT+TEST=RXLRPKT')
    return readData()

def loraConf(id, port):
    if connectTest() != '+AT: OK': 
        return 0
    sendAT('AT+RESET')
    sendAT('AT+MODE=TEST')
    #sendAT('AT+CH=1-3')
    #sendAT(f'AT+ID=DevAddr, "{id}"')
    #sendAT('AT+PORT={port}')
    return 1
    
    

def main():
    receiveData()
    



if __name__ == "__main__":
    if loraConf("00 01 0F 2C", 8) == 0:
        exit()
    while True:
        main()