
import time

import random
# from ucollections import deque
from collections import deque

from finite_machine import proximity_sensors_event
from finite_machine import button

class Event_trigger(object):
    button_a_triggered = 'button_a_triggered'
    button_b_triggered = 'button_b_triggered'
    button_c_triggered = 'button_c_triggered'
    line_low_limit = 400
    line_high_limit = 600
    line_low_triggers = [
        'line_0_low_triggered',
        'line_1_low_triggered',
        'line_2_low_triggered',
        'line_3_low_triggered',
        'line_4_low_triggered',
    ]
    line_high_triggers = [
        'line_0_high_triggered',
        'line_1_high_triggered',
        'line_2_high_triggered',
        'line_3_high_triggered',
        'line_4_high_triggered',
    ]
    timeout_triggered = 'timeout_triggered'
    timeout_triggers = [
        'timeout_triggered0',
        'timeout_triggered1',
        'timeout_triggered2',
        'timeout_triggered3',
        'timeout_triggered4',
    ]
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
    angle_triggered = 'angle_triggered'

    done_triggered = 'done_triggered'


class Buttons(object):
    def __init__(self, display):
        self.display = display
        self.button_a = button.ButtonA()
        self.button_a.debounce_ms = 5
        self.button_a.long_press_ms = 75
        self.button_b = button.ButtonB()
        self.button_b.debounce_ms = 5
        self.button_b.long_press_ms = 75
        self.button_c = button.ButtonC()
        self.buttons = [self.button_a, self.button_b, self.button_c]
        self.buttons_release()
        self.buttons_pressed = deque((), 10)
        self.buttons_list = [False, False, False]

    def buttons_release(self):
        for button_set in self.buttons:
            button_set.debounce_ms = 500
            button_set.long_press_ms = 7500

    def clear_buttons(self):
        self.buttons_pressed = deque((), 10)

    def check_button_pressed(self) -> list:
        # if self.button_a.is_pressed():
        #     if not self.buttons_list[0]:
        button_labels = 'abc'

        # print(f'{self.buttons_list=}')
        for button_index in range(len(self.buttons_list)):
            # self.display.text(f'pressed: {button_index}', 0, 14)
            if self.buttons[button_index].is_pressed() and not self.buttons_list[button_index]:
                self.buttons_list[button_index] = True
                if self.buttons[button_index].check():
                    # self.display.text(f'bp:{button_labels[button_index]}', 0, 14)
                    self.buttons_pressed.append(button_labels[button_index])
            elif not self.buttons[button_index].is_pressed():
                self.buttons_list[button_index] = False
        return self.buttons_list

    def get_button_pressed(self) -> str:
        """
        Return button pressed: button_a_triggered
        """
        if len(self.buttons_pressed) > 0:
            return f'button_{self.buttons_pressed.popleft()}_triggered'
        else:
            return None

    def is_pressed(self) -> list:
        # self.button_a.check()
        # return ['1','2','3']
        return [self.button_a.is_pressed(),
               self.button_b.is_pressed(),
               self.button_c.is_pressed()]

class LineEvents(object):
    """
    line sensor return list[5] with values 0 - 5
    """
    line_low_limit = 500
    line_high_limit = 600
    def __init__(self, _display, _line_sensors):
        """

        line sensor is between 100 to 1024
        """
        self.display = _display
        self.line_sensors = _line_sensors
        self.line = [0,0,0,0,0]
        # self.line_last_trigger =
        self.line_trigger = 5*['init']

    def read(self):
        triggered = []
        line_trigger = self.line_trigger.copy()
        self.line = self.line_sensors.read()
        for index in range(len(self.line)):
            if self.line[index] >= self.line_high_limit:
                if self.line_trigger[index] != 'high':
                    self.line_trigger[index] = 'high'
                    triggered += Event_trigger.line_high_triggers[index]
            elif self.line[index] <= self.line_low_limit:
                if self.line_trigger[index] != 'low':
                    self.line_trigger[index] = 'low'
                    triggered += Event_trigger.line_low_triggers[index]
        # print(f'{triggered=}')
        return triggered

    def reset_trigger(self):
        self.line_trigger = 5*['init']


class CheckEvents(object):
    def __init__(self, _state_matrix, _timer, _display, _line_sensors, _proximity_sensors, _angular_event):
        self.eventSet = set()
        self.display = _display
        # self.events = _events
        self.state_matrix = _state_matrix
        self.not_halted = True
        self.triggered = False
        self.not_triggered = True
        self.log = []
        self.timer = _timer
        self.buttons = Buttons(_display)
        self.lineEvents = LineEvents(_display, _line_sensors)
        self.timeout_triggered = Event_trigger.timeout_triggers[0]
        self.proximity_sensors = _proximity_sensors
        self.triggered_events = set()
        self.angular_event = _angular_event

    def check_events(self):
        self.triggered_events.add(self.timer.event_triggered())
        button_event_list = self.buttons.check_button_pressed()
        button_event = self.buttons.get_button_pressed()
        if button_event is not None:
            # self.display.text(f'be:{button_event}', 0, 14)
            self.triggered_events.add(button_event)
        line_events = self.lineEvents.read()
        # print(f'{line_events=}')
        self.triggered_events.update(line_events)
        proximity_triggers = self.proximity_sensors.check_distance()
        self.triggered_events.update(proximity_triggers)
        angular_event = self.angular_event.check_angle()
        self.triggered_events.update(angular_event)
        # print(f'{self.triggered_events=}')
        return

    def triggered_event(self, _state_events) -> str:
        state_events = set(_state_events.keys())
        triggered = self.triggered_events.intersection(state_events)
        self.triggered_events -= triggered
        if len(triggered) > 0:
            print(f'triggered={list(triggered)}')

        if len(triggered) == 0:
            return None
        else:
            return triggered.pop()

    def clear_events(self):
        self.triggered_events = set()
        self.lineEvents.reset_trigger()
        return

def prompt_event(_state, _events) -> bool:
    text = input(f"Event:")
    return False


class Timer(object):
    def __init__(self):
        self.timeout_counts = 0
        self.timeout_end: float = 0.0

    def start(self, delta :float=1, _count=0):
        self.timeout_counts = _count
        self.timeout_end = time.ticks_add(time.ticks_us(), int(delta*1000)) # int(delta*1000))

    def event_triggered(self):
        if self.timeout_end != 0.0:
            if self.timeout_end < time.ticks_us():
                self.timeout_end = 0.0
                counts = random.randint(0, self.timeout_counts)
                triggered = (Event_trigger.timeout_triggered +
                           str(counts))
                return triggered
        return None

class AngularEvent(object):
    max_speed = 6000
    kp = 350
    kd = 7

    def __init__(self, _robot):
        self.display = None
        self.imu = _robot.IMU()
        self.imu.reset()
        self.imu.enable_default()
        self.calibration_start = time.ticks_ms()
        self.stationary_gz = 0.0
        self.reading_count = 1
        self.drive_motors = False
        self.last_time_gyro_reading = None
        self.turn_rate = 0.0  # degrees per second
        self.robot_angle = 0.0
        self.trigger_angle = None

    def calibrate(self, _display):
        self.display = _display
        self.display.fill(0)
        self.display.text("Calibrating...", 0, 0, 1)
        self.display.show()
        time.sleep_ms(500)
        while time.ticks_diff(time.ticks_ms(), self.calibration_start) < 1000:
            if self.imu.gyro.data_ready():
                self.imu.gyro.read()
                self.stationary_gz += self.imu.gyro.last_reading_dps[2]
                self.reading_count += 1
        self.stationary_gz /= self.reading_count

    def start(self, _trigger_angle):
        self.trigger_angle = _trigger_angle + self.robot_angle
        pass

    def check_angle(self) -> list[str]:
        if self.trigger_angle is not None:
            if self.imu.gyro.data_ready():
                self.imu.gyro.read()
                turn_rate = self.imu.gyro.last_reading_dps[2] - stationary_gz  # degrees per second
                now = time.ticks_us()
                if self.last_time_gyro_reading:
                    dt = time.ticks_diff(now, self.last_time_gyro_reading)
                    self.robot_angle += turn_rate * dt / 1000000
                self.last_time_gyro_reading = now
            if self.trigger_angle < self.robot_angle:
                self.trigger_angle = None
                return [Event_trigger.angle_triggered]
        return []

