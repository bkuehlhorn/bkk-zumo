class FSM():
    led_seconds =   1000 # micro ticks
    drive_seconds = 2000
    line_seconds =  6000
    sensor_seconds = 500
    spin_seconds =  500
    drive_spin = 1000
    spin_speed = 1000
    drive_speed = 3000
    # imu_display, line, line_display, prox, prox_display
    display_details = "prox_display"
    logging = True

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
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.button_c_triggered: "done",
                self.events.Event_trigger.done_triggered: "done"
            },
            "check_line": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.button_c_triggered: "done",
                self.events.Event_trigger.button_a_triggered: "clear_led",
                self.events.Event_trigger.sensor_left_left_closer_triggered: "left_left_closer",
                self.events.Event_trigger.sensor_left_right_closer_triggered: "left_right_closer",
                self.events.Event_trigger.sensor_front_left_closer_triggered: "front_left_closer",
                self.events.Event_trigger.sensor_front_right_closer_triggered: "front_right_closer",
                self.events.Event_trigger.sensor_right_left_closer_triggered: "right_left_closer",
                self.events.Event_trigger.sensor_right_right_closer_triggered: "right_right_closer",
                self.events.Event_trigger.sensor_left_left_farther_triggered: "left_left_farther",
                self.events.Event_trigger.sensor_left_right_farther_triggered: "left_right_farther",
                self.events.Event_trigger.sensor_front_left_farther_triggered: "front_left_farther",
                self.events.Event_trigger.sensor_front_right_farther_triggered: "front_right_farther",
                self.events.Event_trigger.sensor_right_left_farther_triggered: "right_left_farther",
                self.events.Event_trigger.sensor_right_right_farther_triggered: "right_right_farther",
            },
            "clear_led": {
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },

            "left_left_closer": {
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
                self.events.Event_trigger.timeout_triggers[1]: "forward",
            },
            "left_right_closer": {
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
                self.events.Event_trigger.timeout_triggers[1]: "forward",
            },
            "front_left_closer": {
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
                self.events.Event_trigger.timeout_triggers[1]: "forward",
            },
            "front_right_closer": {
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
                self.events.Event_trigger.timeout_triggers[1]: "forward",
            },
            "right_left_closer": {
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
                self.events.Event_trigger.timeout_triggers[1]: "forward",
            },
            "right_right_closer": {
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
                self.events.Event_trigger.timeout_triggers[1]: "forward",
            },
            "left_left_farther": {
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
                self.events.Event_trigger.timeout_triggers[1]: "forward",
            },
            "left_right_farther": {
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
                self.events.Event_trigger.timeout_triggers[1]: "forward",
            },
            "front_left_farther": {
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
                self.events.Event_trigger.timeout_triggers[1]: "forward",
            },
            "front_right_farther": {
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
                self.events.Event_trigger.timeout_triggers[1]: "forward",
            },
            "right_left_farther": {
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
                self.events.Event_trigger.timeout_triggers[1]: "forward",
            },
            "right_right_farther": {
                self.events.Event_trigger.button_b_triggered: "check_line",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
                self.events.Event_trigger.timeout_triggers[1]: "forward",
            },
            "spin_left": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "spin_right": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "forward": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "done": {
                self.events.Event_trigger.timeout_triggers[0]: "done",
            },
        }

        self.state = "init"
        # logging = fsm_logging()
        self.checkEvents = self.events.CheckEvents(self.stateMatrix, self.timer_action_event, self.display,
                                                   self.lineSensors, self.proximity_sensors, self.angular_event)

        self.actionMatrix = {
            "init": [
                (self.actions.display_state, ()),
                (self.actions.off_leds, ()),
                (self.actions.display_text, ("init",)),
                (self.actions.set_leds, (2, 100, 1, 1)),
                (self.actions.forward, (0,))
            ],
            "check_line": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (1, 100, 100, 100)),
                # (self.actions.set_leds, (2, 1, 1, 100)),
                (self.timer_action_event.start, (self.line_seconds,)),
                # (self.actions.spin_left, (self.drive_speed,)),
            ],
            "clear_led": [
                (self.actions.display_state(), ()),
                (self.actions.off_leds, ()),
                (self.timer_action_event.start, (self.line_seconds,)),
            ],
            "left_left_closer": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (5, 100, 1, 100)),
                (self.timer_action_event.start, (self.spin_seconds, 1)),
                (self.actions.spin_left, (self.spin_speed,)),
            ],
            "left_right_closer": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (3, 100, 1, 100)),
                (self.timer_action_event.start, (self.spin_seconds, 1)),
                (self.actions.spin_left, (self.spin_speed,)),
            ],
            "front_left_closer": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (4, 100, 1, 100)),
                (self.timer_action_event.start, (self.spin_seconds, 1)),
                (self.actions.spin_left, (self.spin_speed,)),
            ],
            "front_right_closer": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (4, 100, 1, 100)),
                (self.timer_action_event.start, (self.spin_seconds, 1)),
                (self.actions.spin_right, (self.spin_speed,)),
            ],
            "right_left_closer": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (3, 100, 1, 100)),
                (self.timer_action_event.start, (self.spin_seconds, 1)),
                (self.actions.spin_right, (self.spin_speed,)),
            ],
            "right_right_closer": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (2, 100, 1, 100)),
                (self.timer_action_event.start, (self.spin_seconds, 1)),
                (self.actions.spin_right, (self.spin_speed,)),
            ],
            "left_left_farther": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (5, 100, 1, 1)),
                (self.timer_action_event.start, (self.sensor_seconds, 1)),
                (self.actions.left, (self.drive_speed,)),
            ],
            "left_right_farther": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (3, 100, 1, 1)),
                (self.timer_action_event.start, (self.sensor_seconds, 1)),
                (self.actions.forward, (self.drive_speed,)),
            ],
            "front_left_farther": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (4, 100, 1, 1)),
                (self.timer_action_event.start, (self.sensor_seconds, 1)),
                (self.actions.forward, (self.drive_speed,)),
            ],
            "front_right_farther": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (4, 1, 1, 100)),
                (self.timer_action_event.start, (self.sensor_seconds, 1)),
                (self.actions.forward, (self.drive_speed,)),
            ],
            "right_left_farther": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (3, 100, 1, 1)),
                (self.timer_action_event.start, (self.sensor_seconds, 1)),
                (self.actions.spin_right, (self.spin_speed,)),
            ],
            "right_right_farther": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (2, 100, 1, 1)),
                (self.timer_action_event.start, (self.sensor_seconds, 1)),
                (self.actions.right, (self.drive_spin,)),
            ],
            "spin_left": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (0, 100, 100, 1)),
                (self.actions.set_leds, (2, 1, 1, 100)),
                (self.timer_action_event.start, (self.spin_seconds,)),
                (self.actions.spin_left, (self.spin_speed,)),
            ],
            "spin_right": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (0, 100, 1, 1)),
                (self.actions.set_leds, (2, 1, 100, 100)),
                (self.timer_action_event.start, (self.spin_seconds,)),
                (self.actions.spin_right, (self.spin_speed,)),
            ],
            "forward": [
                # (self.actions.display_state, ()),
                (self.actions.set_leds, (4, 100, 100, 100)),
                (self.timer_action_event.start, (self.drive_seconds,)),
                (self.actions.forward, (self.spin_speed,)),
            ],
            "done": [
                (self.actions.done_action,),
                (self.actions.display_state, ()),
                (self.actions.off_leds,), ]
        }
