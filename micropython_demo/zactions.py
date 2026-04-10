# from unittest import case

# This example shows how to read the three buttons on the Pololu Zumo 2040
# Robot.  It configures button A with an unusually high debounce time of
# 500 ms so you can see the debouncing effect by pressing the button
# quickly.

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

from collections import deque

buffer_len = 15

max_timeout = 5
min_timeout = 1

def display_text(_text):
    display.text(_text, 0, 0)
    print(f"{_text=}")

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

class StateAction(object):
    def __init__(self, _actions, _display):
        self.display = _display
        display = _display
        self.actions = _actions
        self.not_triggered = True
        self.triggered = None
        self.not_halted = True
        rgb_leds.set_brightness(5)

    def do_actions(self, _state):
        if _state == "done":
            self.not_halted = False
            return
        display.text(_state, 0, 0)
        self.display.text(_state, 0, 44)

        for action in self.actions[_state]:
            action[0](*action[1])
        return

    # def get_actions(self, _state) -> list:
    #     if _state == "done":
    #         self.not_halted = False
    #     return self.actions.get(_state, None)


# def print_state(_state, _event, _args) -> int:
#     print(f"{_state=} with {_event}")
#     return 10


def done_action(_state, _event, _args) -> int:
    print(f"{_state=} with {_event}, args={_args}")
    return _args[0]

