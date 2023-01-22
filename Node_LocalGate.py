from Node_functions import loraConf, create_sensor_list, get_sensor_soil, create_valve_list, send_data_hex, getLora, UNIVERSAL_MODE, MAIN_ID, VALVE_ID
from time import sleep, time
from operations import SensorNode, ValveNode, Nodes
from rpi_server_comm import update_sensor, update_valve
from get_weather import get_rain_sum
from random import randrange

MY_ID = MAIN_ID

if __name__ == "__main__":
    if loraConf() == 0:
        print("Error occured: connecting error")
        exit()
    
    last_time = time()
    time_left = 0
    sensor = SensorNode(None, None, None, None, None)
    valve = ValveNode(None, None, None)
    nodes = Nodes()
    soil_avg = 0
    
    rx_sensor_packets = 0
    rx_valve_packets = 0
    tx_valve_packets = 0
    
    time_stamp = time()
    delta_time = 0
    
    while True:
        try:
            sensor_id_list = create_sensor_list(MY_ID)
            valve_id_list = create_valve_list(MY_ID)
            
            # print(f'Lista sensorów: {sensor_id_list}')
            # print(f'Lista zaworów: {valve_id_list}')
            
            nodes = getLora(UNIVERSAL_MODE, sensor_id_list, valve_id_list)

            # forecast_rain = get_rain_sum()
            # soil_avg = get_sensor_soil(MY_ID)
            
            if nodes != None:
                if nodes.SensorNode != None:
                    sensor = nodes.SensorNode
                    sensor.print_data()
                    update_sensor(MY_ID, sensor)
                    soil_avg = sensor.soil_moisture
                    rx_sensor_packets += 1
                        
                if nodes.ValveNode != None:
                    valve = nodes.ValveNode
                    if valve.is_open == 1: valve.is_open = True
                    elif valve.is_open == 0: valve.is_open = False 
                    valve.print_data()
                    update_valve(MY_ID, valve)
                    rx_valve_packets += 1
            
            if soil_avg < 100: need_water = True
            else: need_water = False
            
            if need_water:
                for valve_id in valve_id_list:
                    time_left = 100
                    valve_tmp = ValveNode(valve_id, True, time_left)
                    send_data_hex(valve_tmp.hex_str())
                    print(valve_tmp.hex_str())
                    tx_valve_packets += 1
                    #sleep(randrange(0.5, 1, 0.1))
                    sleep(0.5)
            else:
                for valve_id in valve_id_list:
                    time_left = 0
                    valve_tmp = ValveNode(valve_id, False, time_left)
                    send_data_hex(valve_tmp.hex_str())
                    print(valve_tmp.hex_str())
                    tx_valve_packets += 1
                    #sleep(randrange(0.5, 1, 0.1))
                    sleep(0.5)
                    
            delta_time = time() - time_stamp
            time_stamp = time()
            
            print(f'{delta_time}')
            print(f'Odebrane pakiety sensor: {rx_sensor_packets}')
            print(f'Odebrane pakiety valve: {rx_valve_packets}')
            print(f'Nadane pakiety valve: {tx_valve_packets}\n')
            sleep(0.5)
            
        except KeyboardInterrupt:
            print('\nProgram executed with keyboard interrupt')
            exit()
            