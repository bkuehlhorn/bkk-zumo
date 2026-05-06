class FSM():
    led_seconds =   1000 # micro ticks
    drive_seconds = 2000
    line_seconds =  6000
    sensor_seconds = 500
    spin_seconds =  500
    drive_spin = 1000
    spin_speed = 1000
    drive_speed = 3000

    def __init__(self, _events, _actions, _display, _proximity_sensors, _angular_event, _timer_action_event, _lineSensors, _proximity_sensors_event):
        self.events = _events
        self.actions = _actions
        self.display = _display
        self.proximity_sensors = _proximity_sensors
        self.angular_event = _angular_event
        self.timer_action_event = _timer_action_event
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
                 self.events.Event_trigger.line_low_triggers[0]: "left0l",
                 self.events.Event_trigger.line_high_triggers[0]: "left0h",
                 self.events.Event_trigger.line_low_triggers[1]: "left1l",
                 self.events.Event_trigger.line_high_triggers[1]: "left1h",
                 self.events.Event_trigger.line_low_triggers[2]: "middle4l",
                 self.events.Event_trigger.line_high_triggers[2]: "middle4h",
                 self.events.Event_trigger.line_low_triggers[3]: "right3l",
                 self.events.Event_trigger.line_high_triggers[3]: "right3h",
                 self.events.Event_trigger.line_low_triggers[4]: "right2l",
                 self.events.Event_trigger.line_high_triggers[4]: "right2h",
                 self.events.Event_trigger.button_b_triggered: "init",
                 self.events.Event_trigger.button_c_triggered: "done",
                 self.events.Event_trigger.timeout_triggers[0]: "move_forward",
                 self.events.Event_trigger.timeout_triggers[1]: "move_forward",
                 self.events.Event_trigger.timeout_triggers[2]: "spin_left",
                 self.events.Event_trigger.timeout_triggers[3]: "spin_right",
            },
            "move_left": {
                 self.events.Event_trigger.timeout_triggers[0]: "clear_events",
            },
            "move_right": {
                 self.events.Event_trigger.timeout_triggers[0]: "clear_events",
            },
            "clear_events": {
                 self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "move_forward": {
                 self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "move_backward": {
                 self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "clear_leds": {
                 self.events.Event_trigger.timeout_triggers[0]: "check_line",
            },
            "left0l": {
                 self.events.Event_trigger.timeout_triggers[0]: "move_left",
            },
            "left0h": {
                 self.events.Event_trigger.timeout_triggers[0]: "move_left",
            },
            "left1l": {
                 self.events.Event_trigger.timeout_triggers[0]: "move_left",
            },
            "left1h": {
                 self.events.Event_trigger.timeout_triggers[0]: "move_left",
            },
            "middle4l": {
                 self.events.Event_trigger.timeout_triggers[0]: "clear_leds",
            },
            "middle4h": {
                 self.events.Event_trigger.timeout_triggers[0]: "clear_leds",
            },
            "right3l": {
                 self.events.Event_trigger.timeout_triggers[0]: "move_right",
            },
            "right3h": {
                 self.events.Event_trigger.timeout_triggers[0]: "move_right",
            },
            "right2l": {
                 self.events.Event_trigger.timeout_triggers[0]: "move_right",
            },
            "right2h": {
                 self.events.Event_trigger.timeout_triggers[0]: "move_right",
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
                ( self.actions.off_leds, ()),
                ( self.actions.display_state, ()),
                ( self.actions.set_leds, (1, 100, 1, 1)),
                ( self.actions.forward, (0,)),
            ],
            "check_line": [
                ( self.actions.off_leds, ()),
                ( self.actions.display_state, ()),
                ( self.actions.set_leds, (1, 255, 255, 255)),
                ( self.timer_action_event.start, ( self.line_seconds,3)),
            ],
            "move_backward": [
                ( self.actions.back, ( self.move_speed,)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
            ],
            "move_forward": [
                ( self.actions.forward, ( self.move_speed,)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
            ],
            "move_left": [
                ( self.actions.left, ( self.move_speed,)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
            ],
            "move_right": [
                ( self.actions.right, ( self.move_speed,)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
            ],
            "clear_events": [
                ( self.actions.display_state, ()),
                ( self.actions.off_leds, ()),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                (self.checkEvents.clear_events, ()),
            ],
            "clear_leds": [
                ( self.actions.display_state, ()),
                ( self.actions.off_leds, ()),
                ( self.timer_action_event.start, ( self.line_seconds,)),
            ],
            "left0l": [
                ( self.actions.set_leds, (0, 1, 100, 1)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                ( self.actions.back, ( self.move_speed,)),
            ],
            "left0h": [
                ( self.actions.set_leds, (0, 1, 1, 100)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                ( self.actions.back, ( self.move_speed,)),
            ],
            "left1l": [
                ( self.actions.set_leds, (5, 1, 100, 1)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                ( self.actions.back, ( self.move_speed,)),
            ],
            "left1h": [
                ( self.actions.set_leds, (5, 1, 1, 100)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                ( self.actions.back, ( self.move_speed,)),
            ],
            "middle4l": [
                ( self.actions.set_leds, (4, 1, 100, 1)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                ( self.actions.back, ( self.move_speed,)),
            ],
            "middle4h": [
                ( self.actions.set_leds, (4, 1, 1, 100)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                ( self.actions.back, ( self.move_speed,)),
            ],
            "right3l": [
                ( self.actions.set_leds, (3, 1, 100, 1)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                ( self.actions.back, ( self.move_speed,)),
            ],
            "right3h": [
                ( self.actions.set_leds, (3, 1, 1, 100)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                ( self.actions.back, ( self.move_speed,)),
            ],
            "right2l": [
                ( self.actions.set_leds, (2, 1, 100, 1)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                ( self.actions.back, ( self.move_speed,)),
            ],
            "right2h": [
                ( self.actions.set_leds, (2, 1, 1, 100)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                ( self.actions.back, ( self.move_speed,)),
            ],
            "spin_left": [
                ( self.actions.set_leds, (0, 100, 100, 1)),
                ( self.actions.set_leds, (2, 1, 1, 100)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                ( self.actions.spin_left, ( self.drive_spin,)),
            ],
            "spin_right": [
                ( self.actions.set_leds, (2, 100, 100, 1)),
                ( self.actions.set_leds, (0, 1, 1, 100)),
                ( self.timer_action_event.start, ( self.line_seconds,)),
                ( self.actions.spin_right, ( self.drive_spin,)),
            ],
            "done": [( self.actions.done_action,),
                     ( self.actions.off_leds,),
                     ]
        }
