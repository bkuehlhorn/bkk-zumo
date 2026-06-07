"""
FSM to test button and 6 leds
"""
from finite_machine.zumo_2040_robot import robot

from finite_machine import fsm
from finite_machine import actions
from finite_machine import events
from finite_machine import proximity_sensors_event

display = robot.Display()
lineSensors = robot.LineSensors()
proximity_sensors = proximity_sensors_event.ProximitySensors(robot)
proximity_sensors_triggers = proximity_sensors_event.Triggers()
angular_event = events.AngularEvent(robot)

led_seconds =   1000 # micro ticks
drive_seconds = 2000
line_seconds =  6000
sensor_seconds = 500
spin_seconds =  500
drive_spin = 1000
spin_speed = 1000
drive_speed = 3000
timer_action_event = events.Timer()
timer_action_event.start(drive_seconds)

stateMatrix = {
    "init": {
        events.Event_trigger.button_a_triggered: "spin_left",
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.button_c_triggered: "done",
        events.Event_trigger.done_triggered: "done"
    },
    "check_line": {
        events.Event_trigger.button_b_triggered: "init",
        events.Event_trigger.button_c_triggered: "done",
        events.Event_trigger.button_a_triggered: "clear_led",
        events.Event_trigger.sensor_left_left_closer_triggered: "left_left_closer",
        events.Event_trigger.sensor_left_right_closer_triggered: "left_right_closer",
        events.Event_trigger.sensor_front_left_closer_triggered: "front_left_closer",
        events.Event_trigger.sensor_front_right_closer_triggered: "front_right_closer",
        events.Event_trigger.sensor_right_left_closer_triggered: "right_left_closer",
        events.Event_trigger.sensor_right_right_closer_triggered: "right_right_closer",
        events.Event_trigger.sensor_left_left_farther_triggered: "left_left_farther",
        events.Event_trigger.sensor_left_right_farther_triggered: "left_right_farther",
        events.Event_trigger.sensor_front_left_farther_triggered: "front_left_farther",
        events.Event_trigger.sensor_front_right_farther_triggered: "front_right_farther",
        events.Event_trigger.sensor_right_left_farther_triggered: "right_left_farther",
        events.Event_trigger.sensor_right_right_farther_triggered: "right_right_farther",
    },
    "clear_led": {
        events.Event_trigger.timeout_triggers[0]: "check_line",
    },

    "left_left_closer": {
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.timeout_triggers[0]: "check_line",
        events.Event_trigger.timeout_triggers[1]: "forward",
    },
    "left_right_closer": {
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.timeout_triggers[0]: "check_line",
        events.Event_trigger.timeout_triggers[1]: "forward",
    },
    "front_left_closer": {
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.timeout_triggers[0]: "check_line",
        events.Event_trigger.timeout_triggers[1]: "forward",
    },
    "front_right_closer": {
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.timeout_triggers[0]: "check_line",
        events.Event_trigger.timeout_triggers[1]: "forward",
    },
    "right_left_closer": {
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.timeout_triggers[0]: "check_line",
        events.Event_trigger.timeout_triggers[1]: "forward",
    },
    "right_right_closer": {
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.timeout_triggers[0]: "check_line",
        events.Event_trigger.timeout_triggers[1]: "forward",
    },
    "left_left_farther": {
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.timeout_triggers[0]: "check_line",
        events.Event_trigger.timeout_triggers[1]: "forward",
    },
    "left_right_farther": {
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.timeout_triggers[0]: "check_line",
        events.Event_trigger.timeout_triggers[1]: "forward",
    },
    "front_left_farther": {
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.timeout_triggers[0]: "check_line",
        events.Event_trigger.timeout_triggers[1]: "forward",
    },
    "front_right_farther": {
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.timeout_triggers[0]: "check_line",
        events.Event_trigger.timeout_triggers[1]: "forward",
    },
    "right_left_farther": {
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.timeout_triggers[0]: "check_line",
        events.Event_trigger.timeout_triggers[1]: "forward",
    },
    "right_right_farther": {
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.timeout_triggers[0]: "check_line",
        events.Event_trigger.timeout_triggers[1]: "forward",
    },
    "spin_left": {
        events.Event_trigger.button_b_triggered: "init",
        events.Event_trigger.timeout_triggers[0]: "check_line",
    },
    "spin_right": {
        events.Event_trigger.button_b_triggered: "init",
        events.Event_trigger.timeout_triggers[0]: "check_line",
    },
    "forward": {
        events.Event_trigger.button_b_triggered: "init",
        events.Event_trigger.timeout_triggers[0]: "check_line",
    },
    "done": {
        events.Event_trigger.timeout_triggers[0]: "done",
    },
}
state = "init"

actionMatrix = {
    "init": [
        (actions.display_state, ()),
        (actions.off_leds, ()),
        (actions.display_text, ("init",)),
        (actions.set_leds, (2, 100, 1, 1)),
        (actions.forward, (0,))
    ],
    "check_line": [
        (actions.display_state, ()),
        (actions.set_leds, (1, 100, 100, 100)),
        # (actions.set_leds, (2, 1, 1, 100)),
        (timer_action_event.start, (line_seconds,)),
        # (actions.spin_left, (drive_speed,)),
    ],
    "clear_led": [
        (actions.display_state(), ()),
        (actions.off_leds, ()),
        (timer_action_event.start, (line_seconds,)),
    ],
    "left_left_closer": [
        (actions.display_state, ()),
        (actions.set_leds, (5, 100, 1, 100)),
        (timer_action_event.start, (spin_seconds, 1)),
        (actions.spin_left, (spin_speed,)),
    ],
    "left_right_closer": [
        (actions.display_state, ()),
        (actions.set_leds, (3, 100, 1, 100)),
        (timer_action_event.start, (spin_seconds, 1)),
        (actions.spin_left, (spin_speed,)),
    ],
    "front_left_closer": [
        (actions.display_state, ()),
        (actions.set_leds, (4, 100, 1, 100)),
        (timer_action_event.start, (spin_seconds, 1)),
        (actions.spin_left, (spin_speed,)),
    ],
    "front_right_closer": [
        (actions.display_state, ()),
        (actions.set_leds, (4, 100, 1, 100)),
        (timer_action_event.start, (spin_seconds, 1)),
        (actions.spin_right, (spin_speed,)),
    ],
    "right_left_closer": [
        (actions.display_state, ()),
        (actions.set_leds, (3, 100, 1, 100)),
        (timer_action_event.start, (spin_seconds, 1)),
        (actions.spin_right, (spin_speed,)),
    ],
    "right_right_closer": [
        (actions.display_state, ()),
        (actions.set_leds, (2, 100, 1, 100)),
        (timer_action_event.start, (spin_seconds, 1)),
        (actions.spin_right, (spin_speed,)),
    ],
    "left_left_farther": [
        (actions.display_state, ()),
        (actions.set_leds, (5, 100, 1, 1)),
        (timer_action_event.start, (sensor_seconds, 1)),
        (actions.left, (drive_speed,)),
    ],
    "left_right_farther": [
        (actions.display_state, ()),
        (actions.set_leds, (3, 100, 1, 1)),
        (timer_action_event.start, (sensor_seconds, 1)),
        (actions.forward, (drive_speed,)),
    ],
    "front_left_farther": [
        (actions.display_state, ()),
        (actions.set_leds, (4, 100, 1, 1)),
        (timer_action_event.start, (sensor_seconds, 1)),
        (actions.forward, (drive_speed,)),
    ],
    "front_right_farther": [
        (actions.display_state, ()),
        (actions.set_leds, (4, 1, 1, 100)),
        (timer_action_event.start, (sensor_seconds, 1)),
        (actions.forward, (drive_speed,)),
    ],
    "right_left_farther": [
        (actions.display_state, ()),
        (actions.set_leds, (3, 100, 1, 1)),
        (timer_action_event.start, (sensor_seconds, 1)),
        (actions.spin_right, (spin_speed,)),
    ],
    "right_right_farther": [
        (actions.display_state, ()),
        (actions.set_leds, (2, 100, 1, 1)),
        (timer_action_event.start, (sensor_seconds, 1)),
        (actions.right, (drive_spin,)),
    ],
    "spin_left": [
        (actions.display_state, ()),
        (actions.set_leds, (0, 100, 100, 1)),
        (actions.set_leds, (2, 1, 1, 100)),
        (timer_action_event.start, (spin_seconds,)),
        (actions.spin_left, (spin_speed,)),
    ],
    "spin_right": [
        (actions.display_state, ()),
        (actions.set_leds, (0, 100, 1, 1)),
        (actions.set_leds, (2, 1, 100, 100)),
        (timer_action_event.start, (spin_seconds,)),
        (actions.spin_right, (spin_speed,)),
    ],
    "forward": [
        # (actions.display_state, ()),
        (actions.set_leds, (4, 100, 100, 100)),
        (timer_action_event.start, (drive_seconds,)),
        (actions.forward, (spin_speed,)),
    ],
    "done": [
        (actions.done_action,),
        (actions.display_state, ()),
        (actions.off_leds,), ]
}

# logging = fsm_logging()
checkEvents = events.CheckEvents(stateMatrix, timer_action_event,
                                 display, lineSensors, proximity_sensors, angular_event)
stateActions = actions.StateAction(actionMatrix, display)

fsm = fsm.FSM(checkEvents, stateActions, stateMatrix, robot, display)
fsm.do_fsm()
print("done")
