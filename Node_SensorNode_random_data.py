from Node_functions import loraConf, getSensorData, send_data_hex, SENSOR_ID, SENSOR_SEND_PACKETS
from time import sleep
from random import randrange

MY_ID = SENSOR_ID

if __name__ == "__main__":
    if loraConf() == 0:
        print("Error occured: connecting error")
        exit()
        
    tx_packets = 0
    
    while True:
        try:
            #for i in range [1,SENSOR_SEND_PACKETS]:
            sensor = getSensorData()
            sensor.sensor_id = MY_ID
            print(sensor.hex_str())
            send_data_hex(sensor.hex_str())
            tx_packets += 1
            print(f'Nadane pakiety: {tx_packets}\n')
                #sleep(randrange(0.5, 2, 0.1))
            sleep(0.5)
            
            #sleep(100)
            
        except KeyboardInterrupt:
            print('\nProgram executed with keyboard interrupt')
            exit()
