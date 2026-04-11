"""
FSM to test button and 6 leds
"""
import time
from finite_machine.zumo_2040_robot import robot
display = robot.Display()

import fsm
import zactions, zevents
from finite_machine import fsm
from finite_machine import actions
from finite_machine import events

led_seconds = 2
timer_action_event = events.Timer()
timer_action_event.start()

eventList = [events.prompt_event, timer_action_event.event,
             [events.proximity_event, "closer"],
             [events.proximity_event, "farther"]]
stateMatrix = {
    "init": {
        "event1": "state1",
        "button_b_triggered": "state1",
        "timeout_triggered": "state5",
        "closer": "state2",
        "event_a": "state3",
        "event4": "state4",
        "timeout": "init",
        "done": "done"
    },
    "state1": {
        "init": "state1",
        "button_b_triggered": "state2",
        "timeout_triggered": "init",
        "event1": "init",
        "event2": "state2",
        "event_a": "state3",
        "event4": "state4",
        "timeout": "init",
        "done": "done"
    },
    "state2": {
        "init": "state2",
        "button_b_triggered": "state3",
        "timeout_triggered": "state1",
        "event1": "state1",
        "event2": "init",
        "event3": "state3",
        "event_a": "state4",
        "timeout": "init",
        "done": "done"
    },
    "state3": {
        "init": "state3",
        "button_b_triggered": "state4",
        "timeout_triggered": "state2",
        "event1": "state1",
        "event_a": "state2",
        "event3": "init",
        "event4": "state4",
        "timeout": "init",
        "done": "done"
    },
    "state4": {
        "init": "state4",
        "button_b_triggered": "state5",
        "timeout_triggered": "state3",
        "event_a": "state1",
        "event2": "state2",
        "event3": "init",
        "event4": "state4",
        "timeout": "init",
        "done": "done"
    },
    "state5": {
        "init": "state4",
        "button_b_triggered": "init",
        "timeout_triggered": "state4",
        "event1": "state1",
        "event2": "state2",
        "event3": "init",
        "event_a": "state4",
        "timeout": "init",
        "done": "done"
    },
    "proximity": {
        "init": "state4",
        "timeout_triggered": "init",
        "proximity_triggered": "state4",
        "front_right_closer_triggered": "state1",
        "front_right_farther_triggered": "state2",
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
        "event1": "state1",
        "event2": "state2",
        "event3": "init",
        "event4": "state4",
        "timeout": "init",
        "done": "done"
    },
}
state = "init"
actionMatrix = {
    "init": [(actions.off_leds, ()),
             (actions.display_text, ("init",)),
             (actions.set_leds, (0, 100, 1, 1)),
             (timer_action_event.start, (led_seconds,)),
             ],
    "state1": [(actions.set_leds, (1, 1, 100, 1)),
               (actions.display_text, ("state1",)),
               (timer_action_event.start, (led_seconds,)),
               ],
    "state2": [(actions.set_leds, (2, 1, 1, 100)),
               (actions.display_text, ("state2",)),
               (timer_action_event.start, (led_seconds,)),
               ],
    "state3": [(actions.set_leds, (3, 100, 100, 1)),
               (actions.display_text, ("state3",)),
               (timer_action_event.start, (led_seconds,)),
               ],
    "state4": [(actions.set_leds, (4, 1, 100, 100)),
               (actions.display_text, ("state4",)),
               (timer_action_event.start, (led_seconds,)),
               ],
    "state5": [(actions.set_leds, (5, 100, 100, 100)),
               (actions.display_text, ("state5",)),
               (timer_action_event.start, (led_seconds,)),
               ],
    "done": [(actions.done_action,),
             (actions.off_leds,), ]
}


# logging = fsm_logging()
checkEvents = events.CheckEvents(eventList, timer_action_event, display)
# FSM => matrix[state, event] of nextState
stateActions = actions.StateAction(actionMatrix, display)

fsm = fsm.FSM(checkEvents, stateActions, stateMatrix, robot, display)
fsm.do_fsm()
print("done")