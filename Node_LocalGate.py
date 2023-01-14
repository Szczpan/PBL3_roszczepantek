from Node_functions import loraConf, create_sensor_list, get_sensor_soil, create_valve_list, send_data_hex, getLora, UNIVERSAL_MODE, MAIN_ID, VALVE_ID
from time import sleep, time
from operations import SensorNode, ValveNode, Nodes
from rpi_server_comm import update_sensor, update_valve
from get_weather import get_rain_sum
from random import randrange



if __name__ == "__main__":
    if loraConf() == 0:
        print("Error occured: connecting error")
        exit()
    
    last_time = time()
    time_left = 0
    sensor = SensorNode(None, None, None, None, None)
    valve = ValveNode(None, None, None)
    nodes = Nodes()
    
    while True:
        try:
            sensor_id_list = create_sensor_list(MAIN_ID)
            valve_id_list = create_valve_list(MAIN_ID)
            
            print(f'Lista sensorów: {sensor_id_list}')
            print(f'Lista zaworów: {valve_id_list}')
            
            nodes = getLora(UNIVERSAL_MODE, sensor_id_list, valve_id_list)

            #forecast_rain = get_rain_sum()
            # soil_avg = get_sensor_soil(MAIN_ID)
            soil_avg = randrange(0, 400, 50)
            if nodes != None:
                if nodes.SensorNode != None:
                    sensor = nodes.SensorNode
                    sensor.print_data()
                    if sensor.sensor_id in sensor_id_list:
                        update_sensor(MAIN_ID, sensor)
                        
                if nodes.ValveNode != None:
                    valve = nodes.ValveNode
                    valve.print_data()
                    update_valve(MAIN_ID, valve)
            
            if soil_avg < 200:
                for valve_id in valve_id_list:
                    time_left = 100
                    valve_tmp = ValveNode(valve_id, True, time_left)
                    send_data_hex(valve_tmp.hex_str())
                    sleep(0.5)
                    
            sleep(0.5)
            
        except KeyboardInterrupt:
            print('\nProgram executed with keyboard interrupt')
            exit()
            

            # if nodes != None:
            #     if nodes.SensorNode != None:
            #         sensor = nodes.SensorNode
            #         if soil_avg*forecast_rain < 200:
            #             for valve in valve_id_list:
            #                 valve_obj = ValveNode(valve, True, 100)
            #                 time_left = 100
            #                 update_valve(MAIN_ID, valve_obj)
            #         else:
            #             for valve in valve_id_list:
            #                 valve_obj = ValveNode(valve, False, 0)
            #                 time_left = 0
            #                 update_valve(MAIN_ID, valve_obj)
            #         last_time = time()

            # for valve in valve_id_list:
            #     time_left -= time() - last_time
            #     if time_left > 0:
            #         valve_obj = ValveNode(valve, , time_left)
            #         update_valve(MAIN_ID, valve_obj)
            #         send_data_hex(valve_obj.hex_str())
            #     else:
            #         valve_obj = ValveNode(valve, False, 0)
            #         time_left = 0
            #         update_valve(MAIN_ID, valve_obj)
            #         send_data_hex(valve_obj.hex_str())
            #     last_time = time()
