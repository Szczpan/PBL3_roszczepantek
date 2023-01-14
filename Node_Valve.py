from Node_functions import loraConf, send_data_hex, getLora, VALVE_ID, VALVE_MODE, VALVE_PIN
from operations import ValveNode
from time import sleep
import RPi.GPIO as GPIO

valve = ValveNode(VALVE_ID, False, 0)

if __name__ == "__main__":
    if loraConf() == 0:
        print("Error occured: connecting error")
        exit()
        
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(VALVE_PIN, GPIO.OUT)
    
    while True:
        try:
            nodes = getLora(VALVE_MODE, [], [VALVE_ID])
            
            if nodes != None:
                if nodes.ValveNode != None:
                    valve = nodes.ValveNode
                    valve.valve_id = VALVE_ID
                    valve.print_data()
                    if valve.time_left > 0:
                        GPIO.output(21, GPIO.HIGH)
                        valve.is_open = True
                    elif valve.time_left == 0:
                        GPIO.output(21, GPIO.LOW)
                        valve.is_open = False
                        
            send_data_hex(valve.hex_str())
            print(valve.hex_str)            
            sleep(0.5)
                
        except KeyboardInterrupt:
            print('\nProgram executed with keyboard interrupt')
            exit()
