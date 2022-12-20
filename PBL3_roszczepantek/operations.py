import json
from flask import abort


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


class ValveNode:
    def __init__(self, valve_id, state, time_left):
        self.valve_id = valve_id
        self.state = state
        self.time_left = time_left


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

    return data_json["devices"]


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
    if "main-id" in sensor_body:
        sensor_node_id = sensor_body["sensor-id"]
    else:
        abort(400, "Request body doesn't contain sensor-id field")
        return

    # load data from database file to dictionary
    with open("data.json", 'r') as f:
        data_dict = json.loads(f.read())

    # check if main-id exists



def addValve():
    pass


def getSensor(main_id, sensor_id):
    print(main_id)
    print(sensor_id)


def deleteSensor():
    pass


def getValve():
    pass


def deleteValve():
    pass
