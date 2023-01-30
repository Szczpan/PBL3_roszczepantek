from Node_functions import loraConf, send_data_hex, getLora, VALVE_ID, VALVE_PIN
from operations import ValveNode
from time import time, sleep
from random import randrange
import RPi.GPIO as GPIO

MY_ID = VALVE_ID
valve = ValveNode(MY_ID, False, 0)
time_left = 0
last_time = time()

if __name__ == "__main__":
    if loraConf() == 0:
        print("Error occured: connecting error")
        exit()
        
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(VALVE_PIN, GPIO.OUT)
    
    rx_packets = 0
    tx_packets = 0

    time_stamp = time()
    delta_time = 0
    
    while True:
        try:
            delta_time = time() - time_stamp
            time_stamp = time()
            
            # Gets data from local gate
            nodes = getLora([], [MY_ID])
            
            # If receives data then analyze it and control valve
            if nodes != None:
                if nodes.ValveNode != None:
                    valve = nodes.ValveNode
                    valve.print_data()
                    rx_packets += 1
                    if valve.valve_id == MY_ID:
                        # Opends the valve
                        if valve.time_left > 0:
                            GPIO.output(VALVE_PIN, GPIO.HIGH)
                            valve.is_open = True
                            time_left = valve.time_left
                        # Closes the valve
                        elif valve.time_left == 0:
                            GPIO.output(VALVE_PIN, GPIO.LOW)
                            valve.is_open = False
                            time_left = 0
            
            # Checks if the valve should be opened based on time_left
            if time_left != 0:
                time_left -= time() - last_time
                last_time = time()
                if time_left <= 0: 
                    time_left = 0
                    GPIO.output(VALVE_PIN, GPIO.LOW)
                    valve.is_open = False
            valve.time_left = int(time_left)
            
            # Sends data to local gate
            send_data_hex(valve.hex_str())
            print(valve.hex_str())
            tx_packets += 1
            
            print(f'{delta_time}')
            print(f'Odebrane pakiety valve: {rx_packets}')
            print(f'Nadane pakiety: {tx_packets}\n')    
            
            sleep(randrange(50, 100, 1)/100)        
                
        except KeyboardInterrupt:
            print('\nProgram killed with keyboard interrupt')
            exit()
