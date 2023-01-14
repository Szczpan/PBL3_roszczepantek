from Node_functions import loraConf, create_sensor_list, get_sensor_soil, create_valve_list, send_data_hex, getLora, UNIVERSAL_MODE, MAIN_ID
from time import sleep, time
from operations import SensorNode, ValveNode
from rpi_server_comm import update_sensor, update_valve
from get_weather import get_rain_sum



if __name__ == "__main__":
    if loraConf() == 0:
        print("Error occured: connecting error")
        exit()
    
    last_time = time()
    time_left = 0
    
    while True:
        try:
            sensor_id_list = create_sensor_list(MAIN_ID)
            valve_list = create_valve_list(MAIN_ID)

            received_data = getLora(UNIVERSAL_MODE, sensor_id_list, valve_list)
            sensor = received_data[0]
            valve_trzebazmienicnazwe = received_data[1]

            # print in terminal
            if sensor != 0:
                sensor.print_data

                if sensor.sensor_id in sensor_id_list:
                    update_sensor(MAIN_ID, sensor)
            
            forecast_rain = get_rain_sum()
            soil_avg = get_sensor_soil(MAIN_ID)

            if sensor != 0:
                if soil_avg*forecast_rain < 200:
                    for valve in valve_list:
                        valve_obj = ValveNode(valve, True, 100)
                        time_left = 100
                        update_valve(MAIN_ID, valve_obj)
                else:
                    for valve in valve_list:
                        valve_obj = ValveNode(valve, False, 0)
                        time_left = 0
                        update_valve(MAIN_ID, valve_obj)
                last_time = time()

            for valve in valve_list:
                time_left -= time() - last_time
                if time_left > 0:
                    valve_obj = ValveNode(valve, True, time_left)
                    update_valve(MAIN_ID, valve_obj)
                else:
                    valve_obj = ValveNode(valve, False, 0)
                    time_left = 0
                    update_valve(MAIN_ID, valve_obj)
                last_time = time()

            valve = ValveNode(1, True, 0.1)
            send_data_hex(valve.hex_str)
            
            sleep(0.5)
            
        except KeyboardInterrupt:
            print('\nProgram executed with keyboard interrupt')
            exit()
