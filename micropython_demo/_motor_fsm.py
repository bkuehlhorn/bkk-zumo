"""
FSM to test button and 6 leds
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

drive_sides_seconds = 2
drive_corners_seconds = 1.5
move_speed = 1000

timer_action_event = events.Timer()
timer_action_event.start(1)

stateMatrix = {
    "init": {
        "event1": "forward",
        events.Event_trigger.button_b_triggered: "forward",
        "closer": "left",
        "event_a": "state3",
        "event4": "state4",
        events.Event_trigger.timeout_triggers[0]: "init",
        "done": "done"
    },
    "forward": {
        "init": "forward",
        events.Event_trigger.button_b_triggered: "left",
        events.Event_trigger.timeout_triggers[0]: "left",
        "event2": "left",
        "event_a": "state3",
        "event4": "state4",
        "done": "done"
    },
    "left": {
        "init": "left",
        events.Event_trigger.button_b_triggered: "init",
        events.Event_trigger.timeout_triggers[0]: "forward",
        "event1": "forward",
        "event2": "init",
        "event3": "state3",
        "event_a": "state4",
        "done": "done"
    },
    "state3": {
        "init": "state3",
        events.Event_trigger.button_b_triggered: "state4",
        "event1": "forward",
        "event_a": "left",
        "event3": "init",
        "event4": "state4",
        events.Event_trigger.timeout_triggers[0]: "init",
        "done": "done"
    },
    "state4": {
        "init": "state4",
        events.Event_trigger.button_b_triggered: "state5",
        "event_a": "forward",
        "event2": "left",
        "event3": "init",
        "event4": "state4",
        events.Event_trigger.timeout_triggers[0]: "init",
        "done": "done"
    },
    "state5": {
        "init": "state4",
        events.Event_trigger.button_b_triggered: "init",
        "event1": "forward",
        "event2": "left",
        "event3": "init",
        "event_a": "state4",
        events.Event_trigger.timeout_triggers[0]: "init",
        "done": "done"
    },
    "proximity": {
        "init": "state4",
        events.Event_trigger.timeout_triggers[0]: "init",
        "proximity_triggered": "state4",
        "front_right_closer_triggered": "forward",
        "front_right_farther_triggered": "left",
        "right_closer_triggered": "state3",
        "right_farther_triggered": "state4",
        "front_left_closer_triggered": "state5",
        "front_left_farther_triggered": "state6",
        "left_closer_triggered": "state7",
        "left_farther_triggered": "state8",
        "done": "done"
    },
    "done": {
        "init": "state4",
        "event1": "forward",
        "event2": "left",
        "event3": "init",
        "event4": "state4",
        events.Event_trigger.timeout_triggers[0]: "init",
        "done": "done"
    },
}
state = "init"
actionMatrix = {
    "init": [(actions.off_leds, ()),
             (actions.display_text, ("init",)),
             (actions.set_leds, (0, 100, 1, 1)),
             (timer_action_event.start, (drive_sides_seconds,)),
             (actions.forward, (0,)),
             ],
    "forward": [(actions.off_leds, ()),
                (actions.set_leds, (1, 1, 100, 1)),
                (actions.display_text, ("forward",)),
                (timer_action_event.start, (drive_sides_seconds,)),
                (actions.forward, (move_speed,))
                ],
    "left": [(actions.off_leds, ()),
             (actions.set_leds, (2, 1, 1, 100)),
             (actions.left, (move_speed,)),
             (actions.display_text, ("left",)),
             (timer_action_event.start, (drive_corners_seconds,))
             ],
    "state3": [(actions.set_leds, (3, 100, 100, 1)),
               (actions.display_text, ("state3",)),
               # (timer_action_event.start, (drive_corners_seconds,))
               ],
    "state4": [(actions.set_leds, (4, 1, 100, 100)),
               (actions.display_text, ("state4",)),
               # (timer_action_event.start, (drive_corners_seconds,))
               ],
    "state5": [(actions.set_leds, (5, 100, 100, 100)),
               (actions.display_text, ("state5",)),
               # (timer_action_event.start, (drive_corners_seconds,))
               ],
    "done": [(actions.done_action,),
             (actions.off_leds,), ]
}


# logging = fsm_logging()
checkEvents = events.CheckEvents(stateMatrix, timer_action_event,
                                 display, lineSensors, proximity_sensors)
stateActions = actions.StateAction(actionMatrix, display)

fsm = fsm.FSM(checkEvents, stateActions, stateMatrix, robot, display)
fsm.do_fsm()
print("done")