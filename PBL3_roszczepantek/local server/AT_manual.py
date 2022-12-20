import RPi.GPIO as GPIO
import serial
from time import time, sleep
import sys

uart = serial.Serial("/dev/ttyS0", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=8, timeout=1)

sreadlen = 1024 # max number of chars to read from serial in one try 

def AT_test():
	while True:
		if not uart.inWaiting():
			user_input = input('Insert AT command:  ')
			uart.write((user_input + "\r\n").encode('utf-8'))

		sleep(0.1)
		received_data = ''
		if uart.inWaiting():
			received_data += (uart.read(uart.inWaiting())).decode('utf-8')
			sleep(0.03)
			print(received_data)



if __name__ == "__main__":
	#power_on()
	while True:
		AT_test()
		sleep(5)
