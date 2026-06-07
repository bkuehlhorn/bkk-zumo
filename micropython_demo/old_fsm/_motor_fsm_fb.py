"""
FSM to test button and 6 leds
"""
from finite_machine.zumo_2040_robot import robot

from finite_machine import fsm
from finite_machine import actions
from finite_machine import events
from finite_machine import proximity_sensors_event
from finite_machine.events import Event_trigger

display = robot.Display()
lineSensors = robot.LineSensors()
proximity_sensors = proximity_sensors_event.ProximitySensors(robot)
angular_event = events.AngularEvent(robot)

led_seconds =   1000 # micro ticks
drive_seconds = 1000
drive_spin =    5000
move_speed = 1000
timer_action_event = events.Timer()
timer_action_event.start(drive_seconds)

stateMatrix = {
    "init": {
        "event1": "forward",
        Event_trigger.button_a_triggered: "spin_left",
        Event_trigger.button_b_triggered: "forward",
        Event_trigger.button_c_triggered: "done",
        "done": "done"
    },
    "forward": {
        "init": "forward",
        Event_trigger.button_b_triggered: "init",
        Event_trigger.timeout_triggers[0]: "back",
        Event_trigger.timeout_triggers[1]: "right",
        "done": "done"
    },
    "back": {
        "init": "back",
        Event_trigger.button_b_triggered: "init",
        Event_trigger.timeout_triggers[0]: "forward",
        Event_trigger.timeout_triggers[1]: "left",
        "done": "done"
    },
    "left": {
        "init": "left",
        Event_trigger.button_b_triggered: "init",
        Event_trigger.timeout_triggers[0]: "forward",
        Event_trigger.timeout_triggers[1]: "left",
        "done": "done"
    },
    "right": {
        "init": "left",
        Event_trigger.button_b_triggered: "init",
        Event_trigger.timeout_triggers[0]: "forward",
        Event_trigger.timeout_triggers[1]: "right",
        "done": "done"
    },
    "spin": {
        "init": "right_closer",
        Event_trigger.button_b_triggered: "init",
        Event_trigger.timeout_triggers[0]: "spin_left",
        Event_trigger.timeout_triggers[1]: "spin_right",
    },
    "spin_left": {
        "init": "right_closer",
        Event_trigger.button_b_triggered: "init",
        Event_trigger.timeout_triggers[0]: "init",
    },
    "spin_right": {
        "init": "right_closer",
        Event_trigger.button_b_triggered: "init",
        Event_trigger.timeout_triggers[0]: "init",
    },
    "proximity": {
        "init": "init",
        Event_trigger.timeout_triggers[0]: "init",
        Event_trigger.sensor_front_left_closer_triggered: "left",
        Event_trigger.sensor_front_right_closer_triggered: "right",
        Event_trigger.sensor_left_right_closer_triggered: "left_right",
        Event_trigger.sensor_right_left_closer_triggered: "right_left",
        Event_trigger.sensor_front_left_farther_triggered: "forward_left",
        Event_trigger.sensor_front_right_farther_triggered: "forward_right",
        Event_trigger.sensor_left_right_farther_triggered: "forward",
        Event_trigger.sensor_right_left_farther_triggered: "forward",
        "done": "done"
    },
    "done": {
        Event_trigger.timeout_triggers[0]: "init",
        "done": "done"
    },
}
state = "init"
actionMatrix = {
    "init": [
        (actions.off_leds, ()),
        (actions.display_text, ("init", True)),
        (actions.set_leds, (0, 100, 1, 1)),
        (actions.forward, (0,))
        # (timer_action_event.start, (drive_seconds,))
    ],
    "forward": [
        (actions.off_leds, ()),
        (actions.set_leds, (1, 1, 100, 1)),
        (actions.display_text, ("forward", True)),
        (timer_action_event.start, (drive_seconds,1)),
        (actions.forward, (move_speed,))
    ],
    "back": [
        (actions.off_leds, ()),
        (actions.set_leds, (4, 100, 1, 100)),
        (actions.back, (move_speed,)),
        (actions.display_text, ("back", True)),
        (timer_action_event.start, (drive_seconds,1))
    ],
    "left": [
        (actions.off_leds, ()),
        (actions.set_leds, (5, 100, 100, 1)),
        (actions.left, (move_speed,)),
        (actions.display_text, ("left", True)),
        (timer_action_event.start, (drive_seconds,1))
    ],
    "right": [
        (actions.off_leds, ()),
        (actions.set_leds, (3, 1, 100, 100)),
        (actions.right, (move_speed,)),
        (actions.display_text, ("right", True)),
        (timer_action_event.start, (drive_seconds,1))
    ],
    "left_right": [
        (actions.display_state, ()),
        (timer_action_event.start, (drive_seconds,1))
    ],
    "right_left": [
        (actions.display_state, ()),
        (timer_action_event.start, (drive_seconds,1))
    ],
    "spin": [
        (actions.display_state, ()),
        (timer_action_event.start, (drive_seconds,1))
    ],
    "spin_left": [
        (actions.set_leds, (0, 100, 100, 1)),
        (actions.display_text, ("spin_left", True)),
        (actions.spin_left, (move_speed,)),
        (timer_action_event.start, (drive_spin,1)),
    ],
    "spin_right": [
        (actions.set_leds, (2, 1, 100, 100)),
        (actions.display_text, ("spin_right", True)),
        (actions.spin_right, (move_speed,)),
        (timer_action_event.start, (drive_spin,)),
        (timer_action_event.start, (drive_seconds,1)),
    ],
    "done": [
        (actions.done_action,),
        (actions.off_leds,), ]
}


# logging = fsm_logging()
checkEvents = events.CheckEvents(stateMatrix, timer_action_event,
                                 display, lineSensors, proximity_sensors, angular_event)
stateActions = actions.StateAction(actionMatrix, display)

fsm = fsm.FSM(checkEvents, stateActions, stateMatrix, robot, display)
fsm.do_fsm()
print("done")