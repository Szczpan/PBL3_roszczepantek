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

def main_post():
    pass


def get_all():
    pass


def main_get():
    pass


def slave_node_post():
    pass
