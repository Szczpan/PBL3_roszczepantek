from Node_functions import loraConf, getSensorData, send_data_hex, SENSOR_ID
from time import sleep


    
if __name__ == "__main__":
    if loraConf() == 0:
        print("Error occured: connecting error")
        exit()
    
    while True:
        try:
            sensor = getSensorData()
            sensor.sensor_id = SENSOR_ID
            print(sensor.hex_str())
            send_data_hex(sensor.hex_str())
            
            sleep(5)
            
        except KeyboardInterrupt:
            print('\nProgram executed with keyboard interrupt')
            exit()
