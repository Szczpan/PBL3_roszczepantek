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
    sendAT('AT+MODE=TEST')
    sleep(0.5)
    last_response = sendAT('AT+MODE')
    print(f'Changing LoRa module mode to TEST: {last_response}')
    return 1
    
    

def main():
    last_response = receiveData()
    print(f'Received data: {last_response}')
    last_response = sendAT('AT+MODE')
    print(f'Changing LoRa module mode to TEST: {last_response}')
    
    



if __name__ == "__main__":
    if loraConf("00 01 0F 2C", 8) == 0:
        print("Error occured: connecting error")
        exit()
    while True:
        main()