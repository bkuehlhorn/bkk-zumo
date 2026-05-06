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
                self.events.Event_trigger.timeout_triggers[0]: "state1",
                self.events.Event_trigger.timeout_triggers[1]: "init",
                self.events.Event_trigger.button_b_triggered: "state1",
                self.events.Event_trigger.done_triggered: "done",
            },
            "state1": {
                self.events.Event_trigger.timeout_triggers[0]: "state2",
                self.events.Event_trigger.done_triggered: "done",
                self.events.Event_trigger.timeout_triggers[1]: "init",
            },
            "state2": {
                self.events.Event_trigger.timeout_triggers[0]: "state3",
                self.events.Event_trigger.done_triggered: "done",
                self.events.Event_trigger.timeout_triggers[1]: "init",
            },
            "state3": {
                self.events.Event_trigger.timeout_triggers[0]: "state4",
                self.events.Event_trigger.done_triggered: "done",
                self.events.Event_trigger.timeout_triggers[1]: "init",
            },
            "state4": {
                self.events.Event_trigger.timeout_triggers[0]: "state5",
                self.events.Event_trigger.done_triggered: "done",
                self.events.Event_trigger.timeout_triggers[1]: "init",
            },
            "state5": {
                self.events.Event_trigger.timeout_triggers[0]: "init",
                self.events.Event_trigger.timeout_triggers[1]: "init",
                self.events.Event_trigger.done_triggered: "done",
            },
            "proximity": {
                "init": "state4",
                self.events.Event_trigger.timeout_triggers[0]: "init",
                "proximity_triggered": "state4",
                "front_right_closer_triggered": "state1",
                "front_right_farther_triggered": "state2",
                "right_closer_triggered": "state3",
                "right_farther_triggered": "state4",
                "front_left_closer_triggered": "state5",
                "front_left_farther_triggered": "state6",
                "left_closer_triggered": "state7",
                "left_farther_triggered": "state8",
                "done": "done"
            },
            "done": {
                "init": "state4",
                "event1": "state1",
                "event2": "state2",
                "event3": "init",
                "event4": "state4",
                self.events.Event_trigger.timeout_triggers[0]: "init",
                "done": "done"
            },
        }
        self.state = "init"

        self.checkEvents = self.events.CheckEvents(self.stateMatrix,  self.timer_action_event,
                                                        self.display,  self.lineSensors,  self.proximity_sensors, self.angular_event)

        self.actionMatrix = {
            "init": [(self.actions.off_leds, ()),
                     (self.actions.display_text, ("init",)),
                     (self.actions.set_leds, (0, 100, 1, 1)),
                     (self.timer_action_event.start, (self.led_seconds, 1))],
            "state1": [(self.actions.set_leds, (1, 1, 100, 1)),
                       (self.actions.display_text, ("state1",)),
                       (self.timer_action_event.start, (self.led_seconds, 1))],
            "state2": [(self.actions.set_leds, (2, 1, 1, 100)),
                       (self.actions.display_text, ("state2",)),
                       (self.timer_action_event.start, (self.led_seconds, 1))],
            "state3": [(self.actions.set_leds, (3, 100, 100, 1)),
                       (self.actions.display_text, ("state3",)),
                       (self.timer_action_event.start, (self.led_seconds, 1))],
            "state4": [(self.actions.set_leds, (4, 1, 100, 100)),
                       (self.actions.display_text, ("state4",)),
                       (self.timer_action_event.start, (self.led_seconds, 1))],
            "state5": [(self.actions.set_leds, (5, 100, 100, 100)),
                       (self.actions.display_text, ("state5",)),
                       (self.timer_action_event.start, (self.led_seconds, 1))],
            "done": [(self.actions.done_action,),
                     (self.actions.off_leds,), ]
        }
