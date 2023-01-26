from Node_functions import loraConf, getSensorData, send_data_hex, SENSOR_ID, SENSOR_SEND_PACKETS, VALVE_PIN, DHT11_SENSOR_PIN, MOIST_SENSOR_PIN
from time import time, sleep
import RPi.GPIO as GPIO
from random import randrange


MY_ID = SENSOR_ID


if __name__ == "__main__":
    # Configures LoRa E5 module
    if loraConf() == 0:
        print("Error occured: connecting error")
        exit()
    
    # Initialize GPIO
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DHT11_SENSOR_PIN, GPIO.IN)
    GPIO.setup(MOIST_SENSOR_PIN, GPIO.IN)
    GPIO.setup(VALVE_PIN, GPIO.OUT)
        
    tx_packets = 0
    time_stamp = time()
    delta_time = 0
    
    while True:
        try:
            # Sends data in bursts
            for i in range(SENSOR_SEND_PACKETS):
                # Calculates the time of one full loop
                delta_time = time() - time_stamp
                time_stamp = time()
                
                # Gets data from sensor and saves it to 
                sensor = getSensorData(DHT11_SENSOR_PIN, MOIST_SENSOR_PIN)
                sensor.sensor_id = MY_ID
                
                # Sends data in hex using LoRa
                send_data_hex(sensor.hex_str())
                tx_packets += 1
                
                # Prints actual status
                print(f'Czas od ostatniego wysłania: {delta_time}')
                print(f'Ostatnio wysłany pakiet: {sensor.hex_str()}')
                print(f'Łączna ilość nadanych pakietów: {tx_packets}\n')
                
                # Rests with random time to minimalise interference with other nodes
                sleep(randrange(0, 2, 0.1))
            
            sleep(10)
            
        except KeyboardInterrupt:
            print('\nProgram killed with keyboard interrupt')
            exit()
