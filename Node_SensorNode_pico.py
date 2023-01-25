from machine import Pin
from machine import Timer
from machine import ADC
from machine import UART
import time

moisure = ADC(31)
temperature = ADC(32)
uart = UART(1,baudrate=115200,bits=8,parity=None,stop=1,timeout=1)
uart.init(baudrate=115200,bits=8,parity=None,stop=1,timeout=1)
timer = Timer()
moisureMeas=0
temperatureMeas=0
head=0
nodeID=hex(0).lstrip("0x").zfill(2)
battery=0

# def makeCRC(code):
#     binarycode=bin(code)
    

def measureNsend(timer):
    global moisure
    global temperature
    global uart
    global nodeID
    moisureMeas=hex(moisure.read()).lstrip("0x").zfill(2)
    time.sleep(1)
    temperatureMeas=hex(temperature.read()).lstrip("0x").zfill(2)
    time.sleep(1)
    msg=f'{nodeID}{temperatureMeas}{moisureMeas}'
    uart.write(f'AT+MSGHEX="{msg}"')

def configLora():
    uart.write('AT+RESET')
    time.sleep(5)
    uart.write('AT+ID=DevAddr, "00:01:10:01"')
    time.sleep(2)
    uart.write('AT+CH=2,ON')
    time.sleep(2)

configLora()
timer.init(freq=0.0005, mode=Timer.PERIODIC, callback=measureNsend)
