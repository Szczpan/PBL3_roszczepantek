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


def addMainNode():
    pass


def getAllMainNodes():
    f = open("data.json", 'r')
    data_json = json.loads(f.read())
    f.close()

    for device in data_json["devices"]:
        print(device)

    return data_json["devices"]

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



def deleteSingleMainNode(main_id):
    with open("data.json", 'r') as f:
        data_json = json.loads(f.read())

    for device in data_json["devices"]:
        if main_id in device.values():
            data_json["devices"].remove(device)




def addSensor():
    pass


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
