# from unittest import case

# This example shows how to read the three buttons on the Pololu Zumo 2040
# Robot.  It configures button A with an unusually high debounce time of
# 500 ms so you can see the debouncing effect by pressing the button
# quickly.

import time
from zumo_2040_robot import robot

rgb_leds = robot.RGBLEDs()
rgb_leds.set_brightness(5)
# import button
motors = robot.Motors()
display = robot.Display()
# max = int(motors.MAX_SPEED)
# l_max = int(max * .95)
# r_max = max
# step = max//100
state:str = 'done'

from collections import deque

buffer_len = 15

max_timeout = 5
min_timeout = 1
corner_rate = 4

def display_text(_text, _display_state=False):
    if _display_state:
        display.text(state, 0, 8)
        display.text('_text', 0, 14)
        print(f"state:{state}, text:{_text}")
    display.text(_text, 0, 0)
    # display.text('_textxx', 10, 8)
    print(f"{_text=}")

def display_state():
    display.text(state, 0, 8)
    print(f"state:{state}")

def set_leds(_led, r, g, b):
    rgb_leds.set(_led, [r, g // 3, b])
    rgb_leds.show()

def off_leds():
    for led in range(6):
        rgb_leds.set(led, [0, 0, 0])

def rainbow(hue_start, hue_step, s, v):
    for led in range(6):
        r, g, b = rgb_leds.hsv2rgb(hue_start + hue_step * led, s, v)

        # Green is really bright relative to the other colors;
        # scaling it down 3x makes it look nicer.
        rgb_leds.set(led, [r, g//3, b])
    rgb_leds.show()

def show_leds():
    rgb_leds.show()

def forward(_speed):
    print(f"forward:{_speed=}")
    motors.set_speeds(_speed, _speed)
    return
def back(_speed):
    print(f"back:{_speed=}")
    motors.set_speeds(-_speed, -_speed)
    return
def left(_speed):
    print(f"left:{_speed=}")
    motors.set_speeds(_speed/corner_rate, _speed)
    return
def right(_speed):
    print(f"left:{_speed=}")
    motors.set_speeds(_speed, _speed/corner_rate)
    return
def spin_right(_speed):
    print(f"left:{_speed=}")
    motors.set_speeds(_speed/2, -_speed/2)
    return
def spin_left(_speed):
    print(f"left:{_speed=}")
    motors.set_speeds(-_speed/2, _speed/2)
    return

def sleep(_delay):
    time.sleep(_delay)

class StateAction(object):
    def __init__(self, _actions, _display):
        self.display = _display
        self.actions = _actions
        self.not_triggered = True
        self.triggered = None
        self.not_halted = True
        rgb_leds.set_brightness(5)

    def do_actions(self, _state):
        global state
        state = _state
        if _state == "done":
            self.not_halted = False
            return
        # display.text(_state, 0, 0)
        # self.display.text(_state, 0, 44)

        for action in self.actions[_state]:
            if action is not None:
                action[0](*action[1])
        return

def done_action(_state, _event, _args) -> int:
    print(f"{_state=} with {_event}, args={_args}")
    return _args[0]

