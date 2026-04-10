# This example shows how to read the three buttons on the Pololu Zumo 2040
# Robot.  It configures button A with an unusually high debounce time of
# 500 ms so you can see the debouncing effect by pressing the button
# quickly.

import time
# test fsm
# from zumo_2040_robot import robot

# from line_follower import max_speed

import zactions
import zevents

frame_speed = 1
max_timeout = 5
min_timeout = 1
clock_rate = 2

class Timer():
    def __init__(self):
        self.timeout_end: float = 0.0

    def start(self, delta):
        self.timeout_end = time.time() + delta

    def clear(self):
        self.timeout_end = 0.0

    def event(self):
        if self.timeout_end != 0.0:
            if self.timeout_end < time.time():
                self.timeout_end = 0.0
                return True
        return False


class FSM():
    def __init__(self, _checkEvents, _stateActions, _stateMatrix, _robot, _display):
        # logging = fsm_logging()
        self.checkEvents = _checkEvents
        # FSM => matrix[state, event] of nextState
        self.stateActions = _stateActions
        self.stateMatrix = _stateMatrix
        self.robot = _robot
        self.display = _display
        self.buttons = zevents.Buttons(self.display)
        self.proximity_sensors = self.robot.ProximitySensors()
        self.rgb_leds = self.robot.RGBLEDs()
        self.rgb_leds.set_brightness(2)

        self.show_pressed = False

        self.buffer = ""

        self.timeout = 100
        self.state = "init"
        return

    def do_fsm(self):
        while self.checkEvents.not_halted and self.stateActions.not_halted:
            self.display.fill(0)
            triggeredEvent = self.checkEvents.triggered_event()

            nextState = self.stateMatrix[self.state].get(triggeredEvent, None)
            if nextState is not None:
                self.state = nextState
                self.stateActions.do_actions(self.state)

            self.display.text("RGB demo in fsm", 0, 0)
            self.display.text(f"T:{triggeredEvent}", 0, 28)
            self.display.text(f"S:{nextState}, {int(time.time())}", 0, 36)
            self.display.text("Press B to exit", 0, 56)
            self.display.show()
            zactions.rgb_leds.show()
            if clock_rate > 0:
                time.sleep(clock_rate)
            # else:
            #     input(f"{state}, step")

