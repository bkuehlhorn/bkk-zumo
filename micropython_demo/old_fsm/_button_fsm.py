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
angular_event = events.AngularEvent(robot)

led_seconds = 5000 # micro ticks
timer_action_event = events.Timer()

stateMatrix = {
    "init": {
        events.Event_trigger.button_a_triggered: "proximity",
        events.Event_trigger.button_b_triggered: "state0",
        events.Event_trigger.button_c_triggered: "done",
        events.Event_trigger.timeout_triggers[0]: "state5",
        events.Event_trigger.done_triggered: "done",
    },
    "state0": {
        events.Event_trigger.button_b_triggered: "state1",
        events.Event_trigger.timeout_triggers[0]: "init",
        events.Event_trigger.done_triggered: "done",
    },
    "state1": {
        events.Event_trigger.button_b_triggered: "state2",
        events.Event_trigger.timeout_triggers[0]: "state0",
        events.Event_trigger.done_triggered: "done",
    },
    "state2": {
        events.Event_trigger.button_b_triggered: "state3",
        events.Event_trigger.timeout_triggers[0]: "state1",
        events.Event_trigger.done_triggered: "done",
    },
    "state3": {
        events.Event_trigger.button_b_triggered: "state4",
        events.Event_trigger.timeout_triggers[0]: "state2",
        events.Event_trigger.done_triggered: "done",
    },
    "state4": {
        events.Event_trigger.button_b_triggered: "state5",
        events.Event_trigger.timeout_triggers[0]: "state3",
        events.Event_trigger.done_triggered: "done",
    },
    "state5": {
        "init": "state4",
        events.Event_trigger.button_b_triggered: "init",
        events.Event_trigger.timeout_triggers[0]: "state4",
        events.Event_trigger.done_triggered: "done",
    },
    "proximity": {
        "init": "state4",
        "timeout_triggers[0]": "init",
        proximity_sensors_event.Triggers.sensor_left_left_closer_triggered: "state0",
        proximity_sensors_event.Triggers.sensor_left_right_closer_triggered: "state1",
        proximity_sensors_event.Triggers.sensor_front_left_closer_triggered: "state2",
        proximity_sensors_event.Triggers.sensor_front_right_closer_triggered: "state3",
        proximity_sensors_event.Triggers.sensor_right_left_closer_triggered: "state4",
        proximity_sensors_event.Triggers.sensor_right_right_closer_triggered: "state5",
        events.Event_trigger.done_triggered: "done"
    },
    "done": {
        "done": "done"
    },
}
state = "init"
actionMatrix = {
    "init": [(actions.off_leds, ()),
             (actions.display_text, ("init xxx", True)),
             (timer_action_event.start, (led_seconds,)),
             ],
    "state0": [(actions.set_leds, (0, 100, 0, 0)),
               (actions.display_text, ("state0", True)),
               (timer_action_event.start, (led_seconds,)),
               ],
    "state1": [(actions.set_leds, (1, 0, 100, 0)),
               (actions.display_text, ("state1",)),
               (timer_action_event.start, (led_seconds,)),
               ],
    "state2": [(actions.set_leds, (2, 0, 0, 100)),
               (actions.display_text, ("state2", True)),
               (timer_action_event.start, (led_seconds,)),
               ],
    "state3": [(actions.set_leds, (3, 100, 100, 0)),
               (actions.display_text, ("state3", True)),
               (timer_action_event.start, (led_seconds,)),
               ],
    "state4": [(actions.set_leds, (4, 0, 100, 100)),
               (actions.display_text, ("state4", True)),
               (timer_action_event.start, (led_seconds,)),
               ],
    "state5": [(actions.set_leds, (5, 100, 0, 100)),
               (actions.display_text, ("state5", True)),
               (timer_action_event.start, (led_seconds,)),
               ],
    "proximity": [
               (actions.display_state, ()),
               (timer_action_event.start, (led_seconds,)),
               ],
    "done": [(actions.done_action,),
             (actions.off_leds,), ]
}


# logging = fsm_logging()
checkEvents = events.CheckEvents(stateMatrix, timer_action_event,
                                 display, lineSensors, proximity_sensors, angular_event)
stateActions = actions.StateAction(actionMatrix, display)

fsm = fsm.FSM(checkEvents, stateActions, stateMatrix, robot, display)
fsm.do_fsm()
print("done")