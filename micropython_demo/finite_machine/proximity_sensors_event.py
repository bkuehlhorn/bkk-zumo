import time


class Triggers(object):
    sensor_left_left_closer_triggered = 'sensor_left_closer_triggered'
    sensor_left_left_farther_triggered = 'sensor_left_farther_triggered'
    sensor_left_right_closer_triggered = 'sensor_left_right_closer_triggered'
    sensor_left_right_farther_triggered = 'sensor_left_right_farther_triggered'
    sensor_front_left_closer_triggered = 'sensor_front_left_closer_triggered'
    sensor_front_left_farther_triggered = 'sensor_front_left_farther_triggered'
    sensor_front_right_closer_triggered = 'sensor_front_right_closer_triggered'
    sensor_front_right_farther_triggered = 'sensor_front_right_farther_triggered'
    sensor_right_left_closer_triggered = 'sensor_right_left_closer_triggered'
    sensor_right_left_farther_triggered = 'sensor_right_left_farther_triggered'
    sensor_right_right_closer_triggered = 'sensor_right_right_closer_triggered'
    sensor_right_right_farther_triggered = 'sensor_right_right_farther_triggered'

    def __init__(self):
        return


class ProximitySensors:
    """
    Four sensors to determine abject closer and farther
    Sensor values are from 0 to 5.
    Keep list of prior sensor values
    Save trigger values for closer and farther sensors
    Compare new values with old.

    """
    triggers = Triggers()

    def __init__(self, robot):
        self.proximity_sensors = robot.ProximitySensors()
        self.proximity_left_front = 0
        self.proximity_left = 0
        self.proximity_right_front = 0
        self.proximity_right = 0
        self.sensors = {"left_left": [self.proximity_sensors.left_counts_with_left_leds, 0,
                                      {'closer': [self.triggers.sensor_left_left_closer_triggered],
                                       'farther': [self.triggers.sensor_left_left_farther_triggered],
                                       }],
                        "left_right": [self.proximity_sensors.left_counts_with_right_leds, 0,
                                       {'closer': [self.triggers.sensor_left_right_closer_triggered],
                                        'farther': [self.triggers.sensor_left_right_farther_triggered],
                                        }],
                        "front_left": [self.proximity_sensors.front_counts_with_left_leds, 0,
                                       {'closer': [self.triggers.sensor_front_left_closer_triggered],
                                        'farther': [self.triggers.sensor_front_left_farther_triggered],
                                        }],
                        "front_right": [self.proximity_sensors.front_counts_with_right_leds, 0,
                                        {'closer': [self.triggers.sensor_front_right_closer_triggered],
                                         'farther': [self.triggers.sensor_front_right_farther_triggered],
                                         }],
                        "right_left": [self.proximity_sensors.right_counts_with_left_leds, 0,
                                       {'closer': [self.triggers.sensor_right_left_closer_triggered],
                                        'farther': [self.triggers.sensor_right_left_farther_triggered],
                                        }],
                        "right_right": [self.proximity_sensors.right_counts_with_right_leds, 0,
                                        {'closer': [self.triggers.sensor_right_right_closer_triggered],
                                         'farther': [self.triggers.sensor_right_right_farther_triggered],
                                         }],
                        }
        # self.sensors_keys = list(self.sensors.keys())
        self.sensors_triggers = 6 * ['init']
        self.changes = ['closer', 'farther']

    def check_closer(self, _reading, _value):
        if _reading < _value:
            _value = _reading
            return True
        return False

    def check_farther(self, _reading, _value):
        if _reading > _value:
            _value = _reading
            return True
        return False

    def check_distance(self):
        """
        _sensor: sensor reading, determing which sensor to check
        _direction: sensor direction, checking closer or farther event
        """
        debounce = 1
        proximity_triggers = []
        self.proximity_sensors.read()
        sensor_values = []
        save_sensor_values = []
        for sensor in list(self.sensors.keys()):
            sensor_values += [sensor, self.sensors[sensor][1]]
            current_value = self.sensors[sensor][0]()
            save_sensor_values += [current_value, self.sensors[sensor][1]]
            if current_value > self.sensors[sensor][1]+debounce:
                proximity_triggers += self.sensors[sensor][2]['closer']
                self.sensors[sensor][1] = current_value
            elif current_value < self.sensors[sensor][1]-debounce:
                proximity_triggers += self.sensors[sensor][2]['farther']
                self.sensors[sensor][1] = current_value
        return proximity_triggers

    def trigger(self, side, change) -> bool:
        """
        side: left, left front, right front, right front
        change: closer, farther

        """
        return self.check_closer(self.sensors[side][0](), self.sensors[side][1])
