"""
FSM to test button and 6 leds
"""
from finite_machine.zumo_2040_robot import robot
from finite_machine import events

display = robot.Display()
lineSensors = robot.LineSensors()
angular_event = events.AngularEvent(robot)


from finite_machine import fsm
from finite_machine import actions
from finite_machine import events
from finite_machine import proximity_sensors_event

proximity_sensors = proximity_sensors_event.ProximitySensors(robot)

drive_seconds = 2000
line_seconds = 2000
drive_spin = 500
move_speed = 1000
timer_action_event = events.Timer()
timer_action_event.start(drive_seconds)

stateMatrix = {
    "init": {
        events.Event_trigger.button_a_triggered: "spin_left",
        events.Event_trigger.button_b_triggered: "check_line",
        events.Event_trigger.button_c_triggered: "done",
        "done": "done"
    },
    "check_line": {
        events.Event_trigger.line_low_triggers[0]: "left0l",
        events.Event_trigger.line_high_triggers[0]: "left0h",
        events.Event_trigger.line_low_triggers[1]: "left1l",
        events.Event_trigger.line_high_triggers[1]: "left1h",
        events.Event_trigger.line_low_triggers[2]: "middle4l",
        events.Event_trigger.line_high_triggers[2]: "middle4h",
        events.Event_trigger.line_low_triggers[3]: "right3l",
        events.Event_trigger.line_high_triggers[3]: "right3h",
        events.Event_trigger.line_low_triggers[4]: "right2l",
        events.Event_trigger.line_high_triggers[4]: "right2h",
        events.Event_trigger.button_b_triggered: "init",
        events.Event_trigger.button_c_triggered: "done",
        events.Event_trigger.timeout_triggers[0]: "move_forward",
        events.Event_trigger.timeout_triggers[1]: "move_forward",
        events.Event_trigger.timeout_triggers[2]: "spin_left",
        events.Event_trigger.timeout_triggers[3]: "spin_right",
    },
    "move_left": {
            events.Event_trigger.timeout_triggers[0]: "clear_events",
    },
    "move_right": {
            events.Event_trigger.timeout_triggers[0]: "clear_events",
    },
    "clear_events": {
        events.Event_trigger.timeout_triggers[0]: "check_line",
    },
    "move_forward": {
            events.Event_trigger.timeout_triggers[0]: "check_line",
    },
    "move_backward": {
            events.Event_trigger.timeout_triggers[0]: "check_line",
    },
    "clear_leds": {
        events.Event_trigger.timeout_triggers[0]: "check_line",
    },
    "left0l": {
        events.Event_trigger.timeout_triggers[0]: "move_left",
    },
    "left0h": {
        events.Event_trigger.timeout_triggers[0]: "move_left",
    },
    "left1l": {
        events.Event_trigger.timeout_triggers[0]: "move_left",
    },
    "left1h": {
        events.Event_trigger.timeout_triggers[0]: "move_left",
    },
    "middle4l": {
        events.Event_trigger.timeout_triggers[0]: "clear_leds",
    },
    "middle4h": {
        events.Event_trigger.timeout_triggers[0]: "clear_leds",
    },
    "right3l": {
        events.Event_trigger.timeout_triggers[0]: "move_right",
    },
    "right3h": {
        events.Event_trigger.timeout_triggers[0]: "move_right",
    },
    "right2l": {
        events.Event_trigger.timeout_triggers[0]: "move_right",
    },
    "right2h": {
        events.Event_trigger.timeout_triggers[0]: "move_right",
    },
    "spin_left": {
        events.Event_trigger.timeout_triggers[0]: "move_left",
        events.Event_trigger.timeout_triggers[1]: "move_forward",
    },
    "spin_right": {
        events.Event_trigger.timeout_triggers[0]: "move_right",
        events.Event_trigger.timeout_triggers[1]: "move_forward",
    },
    "done": {
        "done": "done",
    },
}
state = "init"
# logging = fsm_logging()
checkEvents = events.CheckEvents(stateMatrix, timer_action_event,
                                 display, lineSensors, proximity_sensors, angular_event)
actionMatrix = {
    "init": [
        (actions.off_leds, ()),
        (actions.display_state, ()),
        (actions.set_leds, (1, 100, 1, 1)),
        (actions.forward, (0,)),
    ],
    "check_line": [
        (actions.off_leds, ()),
        (actions.display_state, ()),
        (actions.set_leds, (1, 255, 255, 255)),
        (timer_action_event.start, (line_seconds,3)),
    ],
    "move_backward": [
        (actions.back, (move_speed,)),
        (timer_action_event.start, (line_seconds,)),
    ],
    "move_forward": [
        (actions.forward, (move_speed,)),
        (timer_action_event.start, (line_seconds,)),
    ],
    "move_left": [
        (actions.left, (move_speed,)),
        (timer_action_event.start, (line_seconds,)),
    ],
    "move_right": [
        (actions.right, (move_speed,)),
        (timer_action_event.start, (line_seconds,)),
    ],
    "clear_events": [
        (actions.display_state, ()),
        (actions.off_leds, ()),
        (timer_action_event.start, (line_seconds,)),
        (checkEvents.clear_events, ()),
    ],
    "clear_leds": [
        (actions.display_state, ()),
        (actions.off_leds, ()),
        (timer_action_event.start, (line_seconds,)),
    ],
    "left0l": [
        (actions.set_leds, (0, 1, 100, 1)),
        (timer_action_event.start, (line_seconds,)),
        (actions.back, (move_speed,)),
    ],
    "left0h": [
        (actions.set_leds, (0, 1, 1, 100)),
        (timer_action_event.start, (line_seconds,)),
        (actions.back, (move_speed,)),
    ],
    "left1l": [
        (actions.set_leds, (5, 1, 100, 1)),
        (timer_action_event.start, (line_seconds,)),
        (actions.back, (move_speed,)),
    ],
    "left1h": [
        (actions.set_leds, (5, 1, 1, 100)),
        (timer_action_event.start, (line_seconds,)),
        (actions.back, (move_speed,)),
    ],
    "middle4l": [
        (actions.set_leds, (4, 1, 100, 1)),
        (timer_action_event.start, (line_seconds,)),
        (actions.back, (move_speed,)),
    ],
    "middle4h": [
        (actions.set_leds, (4, 1, 1, 100)),
        (timer_action_event.start, (line_seconds,)),
        (actions.back, (move_speed,)),
    ],
    "right3l": [
        (actions.set_leds, (3, 1, 100, 1)),
        (timer_action_event.start, (line_seconds,)),
        (actions.back, (move_speed,)),
    ],
    "right3h": [
        (actions.set_leds, (3, 1, 1, 100)),
        (timer_action_event.start, (line_seconds,)),
        (actions.back, (move_speed,)),
    ],
    "right2l": [
        (actions.set_leds, (2, 1, 100, 1)),
        (timer_action_event.start, (line_seconds,)),
        (actions.back, (move_speed,)),
    ],
    "right2h": [
        (actions.set_leds, (2, 1, 1, 100)),
        (timer_action_event.start, (line_seconds,)),
        (actions.back, (move_speed,)),
    ],
    "spin_left": [
        (actions.set_leds, (0, 100, 100, 1)),
        (actions.set_leds, (2, 1, 1, 100)),
        (timer_action_event.start, (line_seconds,)),
        (actions.spin_left, (drive_spin,)),
    ],
    "spin_right": [
        (actions.set_leds, (2, 100, 100, 1)),
        (actions.set_leds, (0, 1, 1, 100)),
        (timer_action_event.start, (line_seconds,)),
        (actions.spin_right, (drive_spin,)),
    ],
    "done": [(actions.done_action,),
             (actions.off_leds,),
             ]
}


stateActions = actions.StateAction(actionMatrix, display)

fsm = fsm.FSM(checkEvents, stateActions, stateMatrix, robot, display)
fsm.do_fsm()
print("done")