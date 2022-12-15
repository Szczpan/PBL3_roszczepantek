from machine import Pin
from machine import Timer
from machine import ADC
from machine import UART

moisure = ADC(31)
temperature = ADC(32)
uart = UART(1,baudrate=115200,bits=8,parity=None,stop=1,timeout=1)
uart.init(baudrate=115200,bits=8,parity=None,stop=1,timeout=1)
timer = Timer()
moisureMeas=0
temperatureMeas=0
head=0
nodeID=0
battery=0
messageHead=f'AT+MSGHEX="{hex(head).lstrip("0x")}{hex(nodeID).lstrip("0x")}'

def makeCRC(code):
    binarycode=bin(code)
    

def measureNsend(timer):
    global moisure
    global temperature
    moisureMeas=hex(moisure.read()).lstrip("0x")
    temperatureMeas=hex(temperature.read()).lstrip("0x")
    messageMeas=f'{hex(battery).lstrip("0x")}{moisureMeas}{temperatureMeas}'
    CNC=
    uart.write()

#def sendlora (timer):
    #uart.write(buf)
