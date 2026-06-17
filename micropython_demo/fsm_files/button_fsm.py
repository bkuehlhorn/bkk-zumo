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
    display_details = "imu_display"
    logging = True

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
                self.events.Event_trigger.button_a_triggered: "proximity",
                self.events.Event_trigger.button_b_triggered: "state0",
                self.events.Event_trigger.button_c_triggered: "done",
                self.events.Event_trigger.timeout_triggers[0]: "state5",
                self.events.Event_trigger.done_triggered: "done",
            },
            "state0": {
                self.events.Event_trigger.button_b_triggered: "state1",
                self.events.Event_trigger.timeout_triggers[0]: "init",
                self.events.Event_trigger.done_triggered: "done",
            },
            "state1": {
                self.events.Event_trigger.button_b_triggered: "state2",
                self.events.Event_trigger.timeout_triggers[0]: "state0",
                self.events.Event_trigger.done_triggered: "done",
            },
            "state2": {
                self.events.Event_trigger.button_b_triggered: "state3",
                self.events.Event_trigger.timeout_triggers[0]: "state1",
                self.events.Event_trigger.done_triggered: "done",
            },
            "state3": {
                self.events.Event_trigger.button_b_triggered: "state4",
                self.events.Event_trigger.timeout_triggers[0]: "state2",
                self.events.Event_trigger.done_triggered: "done",
            },
            "state4": {
                self.events.Event_trigger.button_b_triggered: "state5",
                self.events.Event_trigger.timeout_triggers[0]: "state3",
                self.events.Event_trigger.done_triggered: "done",
            },
            "state5": {
                self.events.Event_trigger.button_b_triggered: "init",
                self.events.Event_trigger.timeout_triggers[0]: "state4",
                self.events.Event_trigger.done_triggered: "done",
            },
            "proximity": {
                 self.proximity_sensors_event.Triggers.sensor_left_left_closer_triggered: "state0",
                 self.proximity_sensors_event.Triggers.sensor_left_right_closer_triggered: "state1",
                 self.proximity_sensors_event.Triggers.sensor_front_left_closer_triggered: "state2",
                 self.proximity_sensors_event.Triggers.sensor_front_right_closer_triggered: "state3",
                 self.proximity_sensors_event.Triggers.sensor_right_left_closer_triggered: "state4",
                 self.proximity_sensors_event.Triggers.sensor_right_right_closer_triggered: "state5",
                self.events.Event_trigger.done_triggered: "done"
            },
            "done": {
                "done": "done"
            },
        }
        self.state = "init"
        x = self.stateMatrix
        x = self.timer_action_event
        x = self.display
        x = self.lineSensors
        x = self.proximity_sensors_event
        x = self.angular_event
        self.checkEvents = self.events.CheckEvents(self.stateMatrix, self.timer_action_event, self.display,
                                                   self.lineSensors, self.proximity_sensors, self.angular_event)

        self.actionMatrix = {
            "init": [(self.actions.off_leds, ()),
                     (self.actions.display_text, ("init xxx", True)),
                     (self.timer_action_event.start, (self.led_seconds,)),
                     (self.checkEvents.clear_events, ()),
                     ],
            "state0": [(self.actions.set_leds, (0, 100, 0, 0)),
                       (self.actions.display_text, ("state0", True)),
                       (self.timer_action_event.start, (self.led_seconds,)),
                       ],
            "state1": [(self.actions.set_leds, (1, 0, 100, 0)),
                       (self.actions.display_text, ("state1",)),
                       (self.timer_action_event.start, (self.led_seconds,)),
                       ],
            "state2": [(self.actions.set_leds, (2, 0, 0, 100)),
                       (self.actions.display_text, ("state2", True)),
                       (self.timer_action_event.start, (self.led_seconds,)),
                       ],
            "state3": [(self.actions.set_leds, (3, 100, 100, 0)),
                       (self.actions.display_text, ("state3", True)),
                       (self.timer_action_event.start, (self.led_seconds,)),
                       ],
            "state4": [(self.actions.set_leds, (4, 0, 100, 100)),
                       (self.actions.display_text, ("state4", True)),
                       (self.timer_action_event.start, (self.led_seconds,)),
                       ],
            "state5": [(self.actions.set_leds, (5, 100, 0, 100)),
                       (self.actions.display_text, ("state5", True)),
                       (self.timer_action_event.start, (self.led_seconds,)),
                       ],
            "proximity": [
                       (self.actions.display_state, ()),
                       (self.timer_action_event.start, (self.led_seconds,)),
                       ],
            "done": [(self.actions.done_action,),
                     (self.actions.off_leds,), ]
        }
