import requests
from operations import MainDevice, SensorNode, ValveNode
from operations import get_timestamp

SERVER_IP = "http://10.140.123.3:8000/"


def update_sensor(main_id, sensor_node):
    json_to_send = prepare_sensor_json(sensor_node)
    ADDRESS = SERVER_IP + f"api-v1/devices/{main_id}/sensors/{sensor_node.sensor_id}"
    requests.put(ADDRESS, json = json_to_send)


def update_valve(main_id, valve_node):
    json_to_send = prepare_valve_json(valve_node)

    ADDRESS = SERVER_IP + f"api-v1/devices/{main_id}/valves/{valve_node.valve_id}"
    requests.put(ADDRESS, json = json_to_send)


def prepare_valve_json(valve_node):
    valve_json = {
        "valve-id": valve_node.valve_id,
        "state": valve_node.state,
        "time-left": valve_node.time_left
    }
    return valve_json

def prepare_sensor_json(sensor_node):
    sensor_json = {
        "sensor-id": sensor_node.sensor_id,
        "air-humidity": sensor_node.air_humidity,
        "air-temperature": sensor_node.air_temperature,
        "soil-moisture": sensor_node.soil_moisture,
        "battery-level": sensor_node.battery_level
    }
    return sensor_json


if __name__ == "__main__":
    sensor_node = SensorNode(9, 100, 120, 23, 30)
    update_sensor(2, sensor_node)

    valve_node = ValveNode(5, True, 100)
    update_valve(2, valve_node)
