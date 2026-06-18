class FSM():
    led_seconds =   1000 # micro ticks
    drive_seconds = 2000
    line_seconds =  1000
    sensor_seconds = 500
    spin_seconds =  500
    drive_spin = 1000
    spin_speed = 1000
    drive_speed = 1000
    move_speed = 1000
    # imu_display, line, line_display, prox, prox_display
    display_details = "line_display"
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
                "done": "done"
            },
            "check_line": {
                self.events.Event_trigger.line_right_trigger: "right",
                self.events.Event_trigger.line_center_trigger: "center",
                self.events.Event_trigger.line_left_trigger: "left",
                # self.events.Event_trigger.line_low_triggers[0]: "left",
                # self.events.Event_trigger.line_high_triggers[0]: "left",
                # self.events.Event_trigger.line_low_triggers[1]: "left",
                # self.events.Event_trigger.line_high_triggers[1]: "left",
                # self.events.Event_trigger.line_low_triggers[2]: "center",
                # self.events.Event_trigger.line_high_triggers[2]: "center",
                # self.events.Event_trigger.line_low_triggers[3]: "right",
                # self.events.Event_trigger.line_high_triggers[3]: "right",
                # self.events.Event_trigger.line_low_triggers[4]: "right",
                # self.events.Event_trigger.line_high_triggers[4]: "right",
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.button_c_triggered: "done",
                self.events.Event_trigger.timeout_triggers[0]: "move_forward",
                self.events.Event_trigger.timeout_triggers[1]: "move_forward",
                self.events.Event_trigger.timeout_triggers[2]: "spin_left",
                self.events.Event_trigger.timeout_triggers[3]: "spin_right",
            },
            "move_left": {
                self.events.Event_trigger.line_center_trigger: "clear_events",
                self.events.Event_trigger.timeout_triggers[0]: "clear_events",
            },
            "move_right": {
                self.events.Event_trigger.line_center_trigger: "clear_events",
                self.events.Event_trigger.timeout_triggers[0]: "clear_events",
            },
            "clear_events": {
                self.events.Event_trigger.line_center_trigger: "clear_events",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "move_forward": {
                self.events.Event_trigger.line_center_trigger: "clear_events",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "move_backward": {
                self.events.Event_trigger.line_center_trigger: "clear_events",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "clear_leds": {
                self.events.Event_trigger.line_center_trigger: "clear_events",
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "left": {
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "center": {
                self.events.Event_trigger.timeout_triggers[0]: "left",
                self.events.Event_trigger.timeout_triggers[1]: "right",
            },
            "right": {
                self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "spin_left": {
                self.events.Event_trigger.timeout_triggers[0]: "move_left",
                self.events.Event_trigger.timeout_triggers[1]: "move_forward",
            },
            "spin_right": {
                self.events.Event_trigger.timeout_triggers[0]: "move_right",
                self.events.Event_trigger.timeout_triggers[1]: "move_forward",
            },
            "done": {
                "done": "done",
            },
        }

        self.state = "init"
        # logging = fsm_logging()
        self.checkEvents = self.events.CheckEvents(self.stateMatrix, self.timer_action_event, self.display,
                                                   self.lineSensors, self.proximity_sensors, self.angular_event)
        self.actionMatrix = {
            "init": [
                (self.actions.off_leds, ()),
                (self.actions.display_state, ()),
                (self.actions.set_leds, (1, 100, 1, 1)),
                (self.actions.forward, (0,)),
            ],
            "check_line": [
                (self.actions.off_leds, ()),
                (self.actions.display_state, ()),
                (self.actions.set_leds, (1, 255, 255, 255)),
                (self.timer_action_event.start, (self.line_seconds,0)),
                (self.actions.forward, (self.drive_speed,)),
            ],
            "move_left": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (5, 255, 0, 0)),
                (self.actions.left, (self.move_speed,)),
                (self.timer_action_event.start, (self.line_seconds,)),
            ],
            "move_right": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (3, 0, 0, 255)),
                (self.actions.right, (self.move_speed,)),
                (self.timer_action_event.start, (self.line_seconds,)),
            ],
            "move_backward": [
                (self.actions.display_state, ()),
                (self.actions.back, (self.move_speed,)),
                (self.timer_action_event.start, (self.line_seconds,)),
            ],
            "move_forward": [
                (self.actions.display_state, ()),
                (self.actions.forward, (self.move_speed,)),
                (self.timer_action_event.start, (self.line_seconds,)),
            ],
            "clear_events": [
                (self.actions.display_state, ()),
                (self.actions.off_leds, ()),
                (self.timer_action_event.start, (self.line_seconds,)),
                (self.checkEvents.clear_events, ()),
            ],
            "clear_leds": [
                (self.actions.display_state, ()),
                (self.actions.off_leds, ()),
                (self.timer_action_event.start, (self.line_seconds,)),
            ],
            "left": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (5, 100, 1, 1)),
                (self.timer_action_event.start, (self.line_seconds,)),
                (self.actions.right, (self.move_speed,)),
            ],
            "center": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (4, 1, 100, 1)),
                (self.timer_action_event.start, (self.line_seconds, 1)),
                (self.actions.back, (self.move_speed,)),
            ],
            "right": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (3, 1, 1, 100)),
                (self.timer_action_event.start, (self.line_seconds,)),
                (self.actions.left, (self.move_speed,)),
            ],
            "spin_left": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (0, 100, 100, 1)),
                (self.actions.set_leds, (2, 1, 1, 100)),
                (self.timer_action_event.start, (self.line_seconds,)),
                (self.actions.spin_left, (self.drive_spin,)),
            ],
            "spin_right": [
                (self.actions.display_state, ()),
                (self.actions.set_leds, (2, 100, 100, 1)),
                (self.actions.set_leds, (0, 1, 1, 100)),
                (self.timer_action_event.start, (self.line_seconds,)),
                (self.actions.spin_right, (self.drive_spin,)),
            ],
            "done": [(self.actions.done_action,),
                     (self.actions.off_leds,),
                     (self.actions.display_state, ()),
                     ]
        }
