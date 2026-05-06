
led_seconds = 5000 # micro ticks

class Event_trigger(object):
    button_a_triggered = 'button_a_triggered'
    button_b_triggered = 'button_b_triggered'
    button_c_triggered = 'button_c_triggered'
    line_low_limit = 400
    line_high_limit = 600
    line_low_triggers = [
        'line_0_low_triggered',
        'line_1_low_triggered',
        'line_2_low_triggered',
        'line_3_low_triggered',
        'line_4_low_triggered',
    ]
    line_high_triggers = [
        'line_0_high_triggered',
        'line_1_high_triggered',
        'line_2_high_triggered',
        'line_3_high_triggered',
        'line_4_high_triggered',
    ]
    timeout_triggered = 'timeout_triggered'
    timeout_triggers = [
        'timeout_triggered0',
        'timeout_triggered1',
        'timeout_triggered2',
        'timeout_triggered3',
        'timeout_triggered4',
    ]
    sensor_left_left_closer_triggered = 'sensor_left_closer_triggered'
    sensor_left_left_farther_triggered = 'sensor_left_farther_triggered'
    sensor_left_right_closer_triggered = 'sensor_left_right_closer_triggered'
    sensor_left_right_farther_triggered = 'sensor_left_right_farther_triggered'
    sensor_front_left_closer_triggered = 'sensor_front_left_closer_triggered'
    sensor_front_left_farther_triggered = 'sensor_front_left_farther_triggered'
    sensor_front_right_closer_triggered = 'sensor_front_right_closer_triggered'
    sensor_front_right_farther_triggered = 'sensor_front_right_farther_triggered'
    sensor_right_left_closer_triggered = 'sensor_right_left_closer_triggered'
    sensor_right_left_farther_triggered = 'sensor_right_left_farther_triggered'
    sensor_right_right_closer_triggered = 'sensor_right_right_closer_triggered'
    sensor_right_right_farther_triggered = 'sensor_right_right_farther_triggered'
    angle_triggered = 'angle_triggered'

    done_triggered = 'done_triggered'

class proximity_sensors_event():
    class Triggers(object):
        sensor_left_left_closer_triggered = 'sensor_left_closer_triggered'
        sensor_left_left_farther_triggered = 'sensor_left_farther_triggered'
        sensor_left_right_closer_triggered = 'sensor_left_right_closer_triggered'
        sensor_left_right_farther_triggered = 'sensor_left_right_farther_triggered'
        sensor_front_left_closer_triggered = 'sensor_front_left_closer_triggered'
        sensor_front_left_farther_triggered = 'sensor_front_left_farther_triggered'
        sensor_front_right_closer_triggered = 'sensor_front_right_closer_triggered'
        sensor_front_right_farther_triggered = 'sensor_front_right_farther_triggered'
        sensor_right_left_closer_triggered = 'sensor_right_left_closer_triggered'
        sensor_right_left_farther_triggered = 'sensor_right_left_farther_triggered'
        sensor_right_right_closer_triggered = 'sensor_right_right_closer_triggered'
        sensor_right_right_farther_triggered = 'sensor_right_right_farther_triggered'

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
        # Event_trigger.s sensor_back_left_closer_triggered: "right",
        # Event_trigger.sensor_back_right_closer_triggered: "left",
        Event_trigger.sensor_left_right_closer_triggered: "left_right",
        Event_trigger.sensor_right_left_closer_triggered: "right_left",
        Event_trigger.sensor_front_left_farther_triggered: "forward_left",
        Event_trigger.sensor_front_right_farther_triggered: "forward_right",
        # Event_trigger.sensor_back_left_farther_triggered: "back_right",
        # Event_trigger.sensor_back_right_farther_triggered: "back_left",
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
        # (actions.off_leds, ()),
        # (actions.display_text, ("init", True)),
        # (actions.set_leds, (0, 100, 1, 1)),
        # (actions.forward, (0,))
        # (timer_action_event.start, (drive_seconds,))
    ],
    "forward": [
        # (actions.off_leds, ()),
        # (actions.set_leds, (1, 1, 100, 1)),
        # (actions.display_text, ("forward", True)),
        # (timer_action_event.start, (drive_seconds,1)),
        # (actions.forward, (move_speed,))
    ],
    "back": [
        # (actions.off_leds, ()),
        # (actions.set_leds, (4, 100, 1, 100)),
        # (actions.back, (move_speed,)),
        # (actions.display_text, ("back", True)),
        # (timer_action_event.start, (drive_seconds,1))
    ],
    "left": [
        # (actions.off_leds, ()),
        # (actions.set_leds, (5, 100, 100, 1)),
        # (actions.left, (move_speed,)),
        # (actions.display_text, ("left", True)),
        # (timer_action_event.start, (drive_seconds,1))
    ],
    "right": [
        # (actions.off_leds, ()),
        # (actions.set_leds, (3, 1, 100, 100)),
        # (actions.right, (move_speed,)),
        # (actions.display_text, ("right", True)),
        # (timer_action_event.start, (drive_seconds,1))
    ],
    "left_right": [
        # (actions.display_state, ()),
        # (timer_action_event.start, (drive_seconds,1))
    ],
    "right_left": [
        # (actions.display_state, ()),
        # (timer_action_event.start, (drive_seconds,1))
    ],
    "spin": [
        # (actions.display_state, ()),
        # (timer_action_event.start, (drive_seconds,1))
    ],
    "spin_left": [
        # (actions.set_leds, (0, 100, 100, 1)),
        # (actions.display_text, ("spin_left", True)),
        # (actions.spin_left, (move_speed,)),
        # (timer_action_event.start, (drive_spin,1)),
    ],
    "spin_right": [
        # (actions.set_leds, (2, 1, 100, 100)),
        # (actions.display_text, ("spin_right", True)),
        # (actions.spin_right, (move_speed,)),
        # (timer_action_event.start, (drive_spin,)),
        # (timer_action_event.start, (drive_seconds,1)),
    ],
    "done": [
        # (actions.done_action,),
        # (actions.off_leds,),
    ]
}


missing_actions = set# (actionMatrix.keys()) - set# (actionMatrix.keys())

print(missing_actions)

