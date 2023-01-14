import json
from flask import abort
from datetime import datetime


class MainDevice:
    def __init__(self, main_id, sensor_nodes, valve_nodes):
        self.main_id = main_id
        self.sensor_nodes = sensor_nodes
        self.valve_nodes = valve_nodes


class SensorNode:
    def __init__(self, sensor_id, air_humidity, soil_moisture, air_temperature, battery_level):
        self.sensor_id = sensor_id
        self.air_humidity = air_humidity
        self.soil_moisture = soil_moisture
        self.air_temperature = air_temperature
        self.battery_level = battery_level
        self.timestamp = get_timestamp()
        
    def ___str___(self):
        return f'{self.sensor_id}{self.air_humidity}{self.soil_moisture}{self.air_temperature}{self.battery_level}{self.timestamp}'
    
    def hex_str(self):
        hex_node_ID = hex(self.sensor_id).lstrip("0x").zfill(4)
        hex_air_temp = hex(self.air_temperature).lstrip("0x").zfill(2)
        hex_air_hum = hex(self.air_humidity).lstrip("0x").zfill(2)
        hex_soil_moist = hex(self.soil_moisture).lstrip("0x").zfill(2)
        hex_battery_lev = hex(self.battery_level).lstrip("0x").zfill(2)
        
        return f'{hex_node_ID}{hex_air_temp}{hex_air_hum}{hex_soil_moist}{hex_battery_lev}'
    
    def print_data(self):
        print(f'node id: {sensor.sensor_id}')
        print(f'wilgotnosc powietrza: {sensor.air_humidity}')
        print(f'wilgotnosc gleby: {sensor.soil_moisture}')
        print(f'temperatura powietrza: {sensor.air_temperature}') 
        print('\n')


class ValveNode:
    def __init__(self, valve_id, is_open, time_left):
        self.valve_id = valve_id
        self.is_open = is_open
        self.time_left = time_left
        self.timestamp = get_timestamp()

    def __str__(self):
        return f'{self.valve_id}{self.is_open}{self.time_left}{self.timestamp}'
    
    def hex_str(self):
        hex_valve_id = hex(self.valve_id).lstrip("0x").zfill(4)
        hex_is_open = hex(self.is_open).lstrip("0x").zfill(2)
        hex_time_left = hex(self.time_left).lstrip("0x").zfill(2)
        hex_timestamp = hex(self.timestamp).lstrip("0x").zfill(2)
        
        return f'{hex_valve_id}{hex_is_open}{hex_time_left}{hex_timestamp}'


# function to add new node to database json file
# returns whole database
def addMainNode(main_node_dict):
    # check if request body has "main-id" field
    if "main-id" in main_node_dict:
        main_node_id = main_node_dict["main-id"]
    else:
        abort(400, "Request body doesn't contain main-id field")
        return

    # load data from database file to dictionary
    with open("data.json", 'r') as f:
        data_dict = json.loads(f.read())

    # check whether node with given id doesn't already exist
    for device in data_dict["devices"]:
        if device["main-id"] == main_node_id:
            abort(403, f"Main node with ID {main_node_id} already exists")

    # initialise new main device
    new_main_node = MainDevice(main_node_id, [], [])

    # format new device as a dictionary
    new_main_node_dict = {"main-id": new_main_node.main_id,
                          "sensor-nodes": new_main_node.sensor_nodes,
                          "valve-nodes": new_main_node.valve_nodes}

    # add new main node to old dictionary
    data_dict["devices"].append(new_main_node_dict)

    # save new data to file
    with open("data.json", 'w') as f:
        f.write(json.dumps(data_dict))

    return data_dict["devices"]


# returns whole json database
def getAllMainNodes():
    f = open("data.json", 'r')
    data_json = json.loads(f.read())
    f.close()

    for device in data_json["devices"]:
        print(device)

    return data_json


# returns single main node with given main-id if exists
def getSingleMainNode(main_id):
    print(main_id)
    f = open("data.json", 'r')
    data_json = json.loads(f.read())
    f.close()

    for device in data_json["devices"]:
        if main_id in device.values():
            print(device)
            return device

    abort(404, f"Device with ID {main_id} not found")


# deletes single main node based on main-id if exists
# returns remaining database json
def deleteSingleMainNode(main_id):
    with open("data.json", 'r') as f:
        data_json = json.loads(f.read())

    for device in data_json["devices"]:
        if main_id in device.values():
            data_json["devices"].remove(device)

    with open("data.json", 'w') as f:
        f.write(json.dumps(data_json))

    return data_json["devices"]


# add new sensor node to list to given main-id
# requires request body containing sensor node info
# returns whole json database
def addSensor(main_id, sensor_body):
    # get sensor node id from request body
    if "sensor-id" in sensor_body:
        sensor_node_id = sensor_body["sensor-id"]
    else:
        abort(400, "Request body doesn't contain sensor-id field")
        return

    # load data from database file to dictionary
    with open("data.json", 'r') as f:
        data_dict = json.loads(f.read())

    # add new sensor to list if main node exists and doesn't have sensor with given node already attached to it
    for device in data_dict["devices"]:
        if device["main-id"] == main_id:
            for sensor in device["sensor-nodes"]:
                if sensor["sensor-id"] == sensor_node_id:
                    abort(403, f"Sensor node with ID {sensor_node_id} already added to {main_id} main node")
                    return

            new_sensor = SensorNode(sensor_node_id, -1, -1, -1, -1)

            new_sensor_dict = {"sensor-id": new_sensor.sensor_id,
                               "air-humidity": new_sensor.air_humidity,
                               "air-temperature": new_sensor.air_temperature,
                               "soil-moisture": new_sensor.soil_moisture,
                               "battery-level": new_sensor.battery_level,
                               "timestamp": new_sensor.timestamp}
            device["sensor-nodes"].append(new_sensor_dict)

            with open("data.json", 'w') as f:
                f.write(json.dumps(data_dict))
            return data_dict["devices"]

    abort(400, f"Unable to add new sensor with ID {sensor_node_id}")

def addValve(main_id, valve_body):
    # get valve id from request body
    if "valve-id" in valve_body:
        valve_node_id = valve_body["valve-id"]
    else:
        abort(400, "Request body doesn't contain valve-id field")
        return

    # load data from database file to dictionary
    with open("data.json", 'r') as f:
        data_dict = json.loads(f.read())

    # add new valve node to given main node if it exists and doesn't already have this valve node attached
    for device in data_dict["devices"]:
        if main_id == device["main-id"]:
            for valve in device["valve-nodes"]:
                if valve["valve-id"] == valve_node_id:
                    abort(403, f"Valve node with ID {valve_node_id} already attached to main node {main_id}")
                    return

            new_valve = ValveNode(valve_node_id, -1, -1)
            new_valve_dict = {
                "valve-id": new_valve.valve_id,
                "is-open": new_valve.is_open,
                "time-left": new_valve.time_left,
                "timestamp": new_valve.timestamp
            }
            device["valve-nodes"].append(new_valve_dict)

            with open("data.json", 'w') as f:
                f.write(json.dumps(data_dict))

            return data_dict["devices"]

    abort(400, "Unable to add new valve node")


# return info about sensor attached to given main node
def getSensor(main_id, sensor_id):
    data_dict = read_from_json("data.json")

    for device in data_dict["devices"]:
        if main_id == device["main-id"]:
            for sensor in device["sensor-nodes"]:
                if sensor_id == sensor["sensor-id"]:
                    return sensor

    abort(404, f"Device with ID {sensor_id} sensor in ID {main_id} main node not found")


# delete sensor from given main node
def deleteSensor(main_id, sensor_id):
    data_dict = read_from_json("data.json")

    for device in data_dict["devices"]:
        if main_id == device["main-id"]:
            for sensor in device["sensor-nodes"]:
                if sensor_id == sensor["sensor-id"]:
                    device["sensor-nodes"].remove(sensor)
                    with open("data.json", "w") as f:
                        f.write(json.dumps(data_dict))
                    return data_dict["devices"]

    abort(404, f"Sensor with ID {sensor_id} not found in main node with ID {main_id}")


# return all info about valve connected to given main node
def getValve(main_id, valve_id):
    data_dict = read_from_json("data.json")

    for device in data_dict["devices"]:
        if main_id == device["main-id"]:
            for valve in device["valve-nodes"]:
                if valve_id == valve["valve-id"]:
                    return valve

    abort(404, f"Valve with ID {valve_id} not found in main node with ID {main_id}")


# delete valve attached to given main node
def deleteValve(main_id, valve_id):
    data_dict = read_from_json("data.json")

    for device in data_dict["devices"]:
        if main_id == device["main-id"]:
            for valve in device["valve-nodes"]:
                if valve_id == valve["valve-id"]:
                    device["valve-nodes"].remove(valve)
                    with open("data.json", 'w') as f:
                        f.write(json.dumps(data_dict))
                    return data_dict["devices"]

    abort(404, f"Valve with ID {valve_id} not found in main node with ID {main_id}")


def updateSensor(main_id, sensor_id, sensor_body):
    # import json database
    data_dict = read_from_json("data.json")

    # iterate over all sensors in all main nodes to find given sensor node
    for i, device in enumerate(data_dict["devices"]):
        if main_id == device["main-id"]:
            for j, sensor in enumerate(device["sensor-nodes"]):
                if sensor_id == sensor["sensor-id"]:
                    # after finding sensor node, make a new one based on the old one
                    new_sensor_dict = create_sensor_dict(sensor_body, sensor)
                    # check if new sensor node is correct
                    if not new_sensor_dict:
                        abort(400, "Request body doesn't contain sensor ID")
                        return
                    if sensor_id != new_sensor_dict["sensor-id"]:
                        abort(400, f"ID from request body is different from url sensor ID")
                        return

                    # assign new sensor node to main node
                    data_dict["devices"][i]["sensor-nodes"][j] = new_sensor_dict

                    # write to file
                    with open("data.json", 'w') as f:
                        f.write(json.dumps(data_dict))

                    return data_dict["devices"]

    abort(404, f"Sensor node with ID {sensor_id} not found in main node with ID {main_id}")


def create_sensor_dict(sensor_body, old_sensor_dict):
    if "sensor-id" not in sensor_body:
        return {}

    new_sensor_dict = old_sensor_dict

    if "air-humidity" in sensor_body:
        new_sensor_dict["air-humidity"] = sensor_body["air-humidity"]

    if "air-temperature" in sensor_body:
        new_sensor_dict["air-temperature"] = sensor_body["air-temperature"]

    if "soil-moisture" in sensor_body:
        new_sensor_dict["soil-moisture"] = sensor_body["soil-moisture"]

    if "battery-level" in sensor_body:
        new_sensor_dict["battery-level"] = sensor_body["battery-level"]

    new_sensor_dict["timestamp"] = get_timestamp()

    return new_sensor_dict


def updateValve(main_id, valve_id, valve_body):
    # import from json database
    data_dict = read_from_json("data.json")

    print(valve_body)

    # iterate over all sensors in all main nodes to find given valve node
    for i, device in enumerate(data_dict["devices"]):
        if main_id == device["main-id"]:
            for j, valve in enumerate(device["valve-nodes"]):
                if valve_id == valve["valve-id"]:
                    new_valve_dict = create_valve_dict(valve_body, valve)

                    if not new_valve_dict:
                        abort(400, "Request body doesn't contain valve ID")

                    if valve_id != new_valve_dict["valve-id"]:
                        abort(400, "Valve IDs don't match")

                    data_dict["devices"][i]["valve-nodes"][j] = new_valve_dict

                    with open("data.json", 'w') as f:
                        f.write(json.dumps(data_dict))

                    return data_dict["devices"]

    abort(404, f"Valve node with ID {valve_id} not found in main node with ID {main_id}")


def create_valve_dict(valve_body, old_valve_dict):
    if 'valve-id' not in valve_body:
        return {}

    new_valve_dict = old_valve_dict

    if "is-open" in valve_body:
        new_valve_dict["is-open"] = valve_body["is-open"]

    if "time-left" in valve_body:
        new_valve_dict["time-left"] = valve_body["time-left"]

    new_valve_dict["timestamp"] = get_timestamp()

    return new_valve_dict


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_from_json(file):
    with open(file, 'r') as f:
        return json.loads(f.read())
