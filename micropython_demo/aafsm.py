# This example shows how to read the three buttons on the Pololu Zumo 2040
# Robot.  It configures button A with an unusually high debounce time of
# 500 ms so you can see the debouncing effect by pressing the button
# quickly.

# test fsm
from zumo_2040_robot import robot

# from line_follower import max_speed

import zactions
import zevents

# buffer_len = 15

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

# timer_action_event = Timer()
# timer_action_event.start(1)
#
# eventList = [zevents.prompt_event, timer_action_event.event,
#              [zevents.proximity_event, "closer"],
#              [zevents.proximity_event, "farther"]]
# stateMatrix = {
#     "init": {
#         "event1": "state1",
#         "timeout_triggered": "state1",
#         "closer": "state2",
#         "event3": "state3",
#         "event4": "state4",
#         "timeout": "init",
#         "done": "done"
#     },
#     "state1": {
#         "init": "state1",
#         "timeout_triggered": "state2",
#         "event1": "init",
#         "event2": "state2",
#         "event3": "state3",
#         "event4": "state4",
#         "timeout": "init",
#         "done": "done"
#     },
#     "state2": {
#         "init": "state2",
#         "timeout_triggered": "state3",
#         "event1": "state1",
#         "event2": "init",
#         "event3": "state3",
#         "event4": "state4",
#         "timeout": "init",
#         "done": "done"
#     },
#     "state3": {
#         "init": "state3",
#         "timeout_triggered": "state4",
#         "event1": "state1",
#         "event2": "state2",
#         "event3": "init",
#         "event4": "state4",
#         "timeout": "init",
#         "done": "done"
#     },
#     "state4": {
#         "init": "state4",
#         "timeout_triggered": "state5",
#         "event1": "state1",
#         "event2": "state2",
#         "event3": "init",
#         "event4": "state4",
#         "timeout": "init",
#         "done": "done"
#     },
#     "state5": {
#         "init": "state4",
#         "timeout_triggered": "init",
#         "event1": "state1",
#         "event2": "state2",
#         "event3": "init",
#         "event4": "state4",
#         "timeout": "init",
#         "done": "done"
#     },
#     "proximity": {
#         "init": "state4",
#         "timeout_triggered": "init",
#         "proximity_triggered": "state4",
#         "front_right_closer_triggered": "state1",
#         "front_right_farther_triggered": "state2",
#         "right_closer_triggered": "state3",
#         "right_farther_triggered": "state4",
#         "front_left_closer_triggered": "state5",
#         "front_left_farther_triggered": "state6",
#         "left_closer_triggered": "state7",
#         "left_farther_triggered": "state8",
#         "done": "done"
#     },
#     "done": {
#         "init": "state4",
#         "event1": "state1",
#         "event2": "state2",
#         "event3": "init",
#         "event4": "state4",
#         "timeout": "init",
#         "done": "done"
#     },
# }
# state = "init"
# actionMatrix = {
#     "init": [(zactions.off_leds, ()),
#              (zactions.set_leds, (0, 100, 1, 1)),
#              (timer_action_event.start, (1,))],
#     "state1": [(zactions.set_leds, (1, 1, 100, 1)),
#                (timer_action_event.start, (1,))],
#     "state2": [(zactions.set_leds, (2, 1, 1, 100)),
#                (timer_action_event.start, (1,))],
#     "state3": [(zactions.set_leds, (3, 100, 100, 1)),
#                (timer_action_event.start, (1,))],
#     "state4": [(zactions.set_leds, (4, 1, 100, 100)),
#                (timer_action_event.start, (1,))],
#     "state5": [(zactions.set_leds, (5, 100, 100, 100)),
#                (timer_action_event.start, (5,))],
#     "done": [(zactions.done_action,),
#              (zactions.off_leds,),]
# }
from led_fsm import *

# logging = fsm_logging()
checkEvents = zevents.CheckEvents(eventList, timer_action_event)
# FSM => matrix[state, event] of nextState
stateActions = zactions.StateAction(actionMatrix)

display = robot.Display()
buttons = zevents.Buttons(display)
proximity_sensors = robot.ProximitySensors()
rgb_leds = robot.RGBLEDs()
rgb_leds.set_brightness(2)

show_pressed = False

buffer = ""

timeout = 100
while checkEvents.not_halted and stateActions.not_halted:
    triggeredEvent = checkEvents.triggered_event()

    nextState = stateMatrix[state].get(triggeredEvent, None)
    if nextState is not None:
        state = nextState
        stateActions.do_actions(state)

    display.fill(0)
    display.text("RGB demo in fsm", 0, 0)
    display.text("Press B to exit", 0, 56)
    display.show()
    zactions.rgb_leds.show()
    if clock_rate > 0:
        time.sleep(clock_rate)
    else:
        input(f"{state}, step")


# while True:
#     display.fill(0)
#     display.text("RGB demo in fsm", 0, 0)
#     display.text("Press B to exit", 0, 56)
#     display.show()
#
#     time_ms = time.ticks_us() // 1000
#     # zactions.rainbow(time_ms//8, 60, 230 + round(25*math.cos(time_ms/3000)), 255)
#     led_colors = [[1,1,1],[1,100,1],[100,1,1],
#                   [1,1,100],[100,100,1],[1,100,100]]
#     for led in range(len(led_colors)):
#         zactions.set_leds(led, *led_colors[led])
#
#     time.sleep_ms(30)

