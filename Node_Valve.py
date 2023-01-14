from Node_functions import loraConf, send_data_hex, getLora, VALVE_ID, VALVE_MODE, VALVE_PIN
from time import sleep
import RPi.GPIO as GPIO



if __name__ == "__main__":
    if loraConf() == 0:
        print("Error occured: connecting error")
        exit()
        
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(VALVE_PIN, GPIO.OUT)
    
    while True:
        try:
            valve = getLora(VALVE_MODE, [], [VALVE_ID])
            print(valve)
                        
            if valve.time_left > 0:
                GPIO.output(21, GPIO.HIGH)
                valve.is_open = True
                send_data_hex(valve)
            elif valve.time_left == 0:
                GPIO.output(21, GPIO.LOW)
                valve.is_open = False
                send_data_hex(valve)
            
            sleep(0.1)
                
        except KeyboardInterrupt:
            print('\nProgram executed with keyboard interrupt')
            exit()
