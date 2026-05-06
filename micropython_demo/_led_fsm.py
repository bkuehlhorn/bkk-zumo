"""
FSM to test timeout and 6 leds
"""
import time
from finite_machine.zumo_2040_robot import robot

from finite_machine import fsm
from finite_machine import actions
from finite_machine import events
from finite_machine import proximity_sensors_event

display = robot.Display()
lineSensors = robot.LineSensors()
proximity_sensors = proximity_sensors_event.ProximitySensors(robot)
angular_event = events.AngularEvent(robot)

led_seconds = 1000 # micro ticks
timer_action_event = events.Timer()

# stateMatrix = {
#     "init": {
#         events.Event_trigger.timeout_triggers[0]: "state1",
#         events.Event_trigger.timeout_triggers[1]: "init",
#         events.Event_trigger.button_b_triggered: "state1",
#         events.Event_trigger.done_triggered: "done",
#     },
#     "state1": {
#         events.Event_trigger.timeout_triggers[0]: "state2",
#         events.Event_trigger.done_triggered: "done",
#         events.Event_trigger.timeout_triggers[1]: "init",
#     },
#     "state2": {
#         events.Event_trigger.timeout_triggers[0]: "state3",
#         events.Event_trigger.done_triggered: "done",
#         events.Event_trigger.timeout_triggers[1]: "init",
#     },
#     "state3": {
#         events.Event_trigger.timeout_triggers[0]: "state4",
#         events.Event_trigger.done_triggered: "done",
#         events.Event_trigger.timeout_triggers[1]: "init",
#     },
#     "state4": {
#         events.Event_trigger.timeout_triggers[0]: "state5",
#         events.Event_trigger.done_triggered: "done",
#         events.Event_trigger.timeout_triggers[1]: "init",
#     },
#     "state5": {
#         events.Event_trigger.timeout_triggers[0]: "init",
#         events.Event_trigger.timeout_triggers[1]: "init",
#         events.Event_trigger.done_triggered: "done",
#     },
#     "proximity": {
#         "init": "state4",
#         events.Event_trigger.timeout_triggers[0]: "init",
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
#         events.Event_trigger.timeout_triggers[0]: "init",
#         "done": "done"
#     },
# }
# state = "init"
# actionMatrix = {
#     "init": [(actions.off_leds, ()),
#              (actions.display_text, ("init",)),
#              (actions.set_leds, (0, 100, 1, 1)),
#              (timer_action_event.start, (led_seconds, 1))],
#     "state1": [(actions.set_leds, (1, 1, 100, 1)),
#                (actions.display_text, ("state1",)),
#                (timer_action_event.start, (led_seconds, 1))],
#     "state2": [(actions.set_leds, (2, 1, 1, 100)),
#                (actions.display_text, ("state2",)),
#                (timer_action_event.start, (led_seconds, 1))],
#     "state3": [(actions.set_leds, (3, 100, 100, 1)),
#                (actions.display_text, ("state3",)),
#                (timer_action_event.start, (led_seconds, 1))],
#     "state4": [(actions.set_leds, (4, 1, 100, 100)),
#                (actions.display_text, ("state4",)),
#                (timer_action_event.start, (led_seconds, 1))],
#     "state5": [(actions.set_leds, (5, 100, 100, 100)),
#                (actions.display_text, ("state5",)),
#                (timer_action_event.start, (led_seconds, 1))],
#     "done": [(actions.done_action,),
#              (actions.off_leds,), ]
# }


# logging = fsm_logging()
checkEvents = events.CheckEvents(stateMatrix, timer_action_event,
                                 display, lineSensors, proximity_sensors, angular_event)
stateActions = actions.StateAction(actionMatrix, display)

fsm = fsm.FSM(checkEvents, stateActions, stateMatrix, robot, display)
fsm.do_fsm()
print("done")