class FSM():
    led_seconds =   1000 # micro ticks
    drive_seconds = 2000
    line_seconds =  6000
    sensor_seconds = 500
    spin_seconds =  500
    drive_spin = 1000
    spin_speed = 1000
    drive_speed = 3000
    move_speed = 1000
    display_details = "line"

    def __init__(self, _events, _actions, _display, _proximity_sensors, _angular_event, _timer_action_event, _lineSensors, _proximity_sensors_event):
        self.events = _events
        self.actions = _actions
        self.display = _display
        self.proximity_sensors = _proximity_sensors
        self.angular_event = _angular_event
        self.timer_action_event = _timer_action_event
        self.timer_action_event.start(self.drive_seconds)
        self.lineSensors = _lineSensors
        self.proximity_sensors_event = _proximity_sensors_event

        self.stateMatrix = {
            "init": {
                self.events.Event_trigger.button_a_triggered: "spin_left",
                self.events.Event_trigger.button_b_triggered: "forward",
                self.events.Event_trigger.button_c_triggered: "done",
                "done": "done"
            },
            "forward": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "back",
                self.events.Event_trigger.timeout_triggers[1]: "right",
            },
            "back": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "forward",
                self.events.Event_trigger.timeout_triggers[1]: "left",
            },
            "left": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "forward",
                self.events.Event_trigger.timeout_triggers[1]: "left",
            },
            "right": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "forward",
                self.events.Event_trigger.timeout_triggers[1]: "right",
            },
            "left_right": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "forward",
                self.events.Event_trigger.timeout_triggers[1]: "right",
            },
            "right_left": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "forward",
                self.events.Event_trigger.timeout_triggers[1]: "right",
            },
            "forward_left": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "forward",
                self.events.Event_trigger.timeout_triggers[1]: "right",
            },
            "forward_right": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "forward",
                self.events.Event_trigger.timeout_triggers[1]: "right",
            },
            "spin": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "spin_left",
                self.events.Event_trigger.timeout_triggers[1]: "spin_right",
            },
            "spin_left": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "init",
            },
            "spin_right": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "init",
            },
            "proximity": {
                self.events.Event_trigger.timeout_triggers[0]: "init",
                self.events.Event_trigger.sensor_front_left_closer_triggered: "left",
                self.events.Event_trigger.sensor_front_right_closer_triggered: "right",
                self.events.Event_trigger.sensor_left_right_closer_triggered: "left_right",
                self.events.Event_trigger.sensor_right_left_closer_triggered: "right_left",
                self.events.Event_trigger.sensor_front_left_farther_triggered: "forward_left",
                self.events.Event_trigger.sensor_front_right_farther_triggered: "forward_right",
                self.events.Event_trigger.sensor_left_right_farther_triggered: "forward",
                self.events.Event_trigger.sensor_right_left_farther_triggered: "forward",
            },
            "done": {
                self.events.Event_trigger.timeout_triggers[0]: "init",
                "done": "done"
            },
        }
        self.state = "init"
        # logging = fsm_logging()
        self.checkEvents = self.events.CheckEvents(self.stateMatrix, self.timer_action_event, self.display,
                                                   self.lineSensors, self.proximity_sensors, self.angular_event)

        self.actionMatrix = {
            "init": [
                (self.actions.off_leds, ()),
                (self.actions.display_text, ("init", True)),
                (self.actions.set_leds, (0, 100, 1, 1)),
                (self.actions.forward, (0,))
                # (self.timer_action_event.start, (self.drive_seconds,))
            ],
            "forward": [
                (self.actions.off_leds, ()),
                (self.actions.set_leds, (1, 1, 100, 1)),
                (self.actions.display_text, ("forward", True)),
                (self.timer_action_event.start, (self.drive_seconds,1)),
                (self.actions.forward, (self.move_speed,))
            ],
            "back": [
                (self.actions.off_leds, ()),
                (self.actions.set_leds, (4, 100, 1, 100)),
                (self.actions.back, (self.move_speed,)),
                (self.actions.display_text, ("back", True)),
                (self.timer_action_event.start, (self.drive_seconds,1))
            ],
            "left": [
                (self.actions.off_leds, ()),
                (self.actions.set_leds, (5, 100, 100, 1)),
                (self.actions.left, (self.move_speed,)),
                (self.actions.display_text, ("left", True)),
                (self.timer_action_event.start, (self.drive_seconds,1))
            ],
            "right": [
                (self.actions.off_leds, ()),
                (self.actions.set_leds, (3, 1, 100, 100)),
                (self.actions.right, (self.move_speed,)),
                (self.actions.display_text, ("right", True)),
                (self.timer_action_event.start, (self.drive_seconds,1))
            ],
            "left_right": [
                (self.actions.display_state, ()),
                (self.timer_action_event.start, (self.drive_seconds,1))
            ],
            "right_left": [
                (self.actions.display_state, ()),
                (self.timer_action_event.start, (self.drive_seconds,1))
            ],
            "spin": [
                (self.actions.display_state, ()),
                (self.timer_action_event.start, (self.drive_seconds,1))
            ],
            "spin_left": [
                (self.actions.set_leds, (0, 100, 100, 1)),
                (self.actions.display_text, ("spin_left", True)),
                (self.actions.spin_left, (self.move_speed,)),
                (self.timer_action_event.start, (self.drive_spin,1)),
            ],
            "spin_right": [
                (self.actions.set_leds, (2, 1, 100, 100)),
                (self.actions.display_text, ("spin_right", True)),
                (self.actions.spin_right, (self.move_speed,)),
                (self.timer_action_event.start, (self.drive_spin,)),
                (self.timer_action_event.start, (self.drive_seconds,1)),
            ],
            "proximity": [
                (self.actions.set_leds, (2, 1, 100, 100)),
                (self.actions.display_text, ("spin_right", True)),
                (self.actions.spin_right, (self.move_speed,)),
                (self.timer_action_event.start, (self.drive_spin,)),
                (self.timer_action_event.start, (self.drive_seconds,1)),
            ],
            "done": [
                (self.actions.done_action,),
                (self.actions.off_leds,), ]
        }
