from machine import Pin
from machine import Timer
from machine import ADC
from machine import UART
import time
import str

moisure = ADC(31)
temperature = ADC(32)
uart = UART(1,baudrate=115200,bits=8,parity=None,stop=1,timeout=1)
uart.init(baudrate=115200,bits=8,parity=None,stop=1,timeout=1)
timer = Timer()
moisureMeas=0
temperatureMeas=0
head=0
nodeID=hex(0).lstrip("0x")
battery=0
messageHead=f'AT+MSGHEX="{hex(head).lstrip("0x")}{hex(nodeID).lstrip("0x")}'

# def makeCRC(code):
#     binarycode=bin(code)
    

def measureNsend(timer):
    global moisure
    global temperature
    moisureMeas=hex(moisure.read()).lstrip("0x")
    time.sleep(1)
    temperatureMeas=hex(temperature.read()).lstrip("0x")
    time.sleep(1)
    uart.write(f'AT+MSGHEX="{nodeID}{temperatureMeas}{moisureMeas}"')

#def sendlora (timer):
    #uart.write(buf)

timer.init(freq=0.0005, mode=Timer.PERIODIC, callback=measureNsend)
