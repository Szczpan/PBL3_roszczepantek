from Node_functions import loraConf, send_data_hex, getLora, VALVE_ID, VALVE_MODE, VALVE_PIN
from operations import ValveNode
from time import time, sleep
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
            nodes = getLora(VALVE_MODE, [], [MY_ID])
            
            if nodes != None:
                if nodes.ValveNode != None:
                    valve = nodes.ValveNode
                    valve.print_data()
                    rx_packets += 1
                    if valve.valve_id == MY_ID:
                        if valve.time_left > 0:
                            GPIO.output(VALVE_PIN, GPIO.HIGH)
                            valve.is_open = True
                            time_left = valve.time_left
                        elif valve.time_left == 0:
                            GPIO.output(VALVE_PIN, GPIO.LOW)
                            valve.is_open = False
                            time_left = 0
            
            if time_left != 0:
                time_left -= time() - last_time
                last_time = time()
                if time_left <= 0: 
                    time_left = 0
                    GPIO.output(VALVE_PIN, GPIO.LOW)
                    valve.is_open = False
            valve.time_left = int(time_left)
            
            send_data_hex(valve.hex_str())
            sleep(3)
            print(valve.hex_str())
            tx_packets += 1
            
            delta_time = time() - time_stamp
            time_stamp = time()
            
            print(f'{delta_time}')
            print(f'Odebrane pakiety valve: {rx_packets}')
            print(f'Nadane pakiety: {tx_packets}\n')            
                
        except KeyboardInterrupt:
            print('\nProgram executed with keyboard interrupt')
            exit()
