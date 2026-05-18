# This example shows how to read the three buttons on the Pololu Zumo 2040
# Robot.  It configures button A with an unusually high debounce time of
# 500 ms so you can see the debouncing effect by pressing the button
# quickly.

frame_speed = 1
max_timeout = 5
min_timeout = 1
clock_rate = 0
state_delay = 1
move_speed = 0
drive_speed = 0

class FSM():
    def __init__(self, _checkEvents, _stateActions, _stateMatrix, _robot, _display):
        # # logging = fsm_logging()
        # self.checkEvents = _checkEvents
        # # FSM => matrix[state, event] of nextState
        # self.stateActions = _stateActions
        # self.stateMatrix = _stateMatrix
        # self.robot = _robot
        # self.display = _display
        # self.buttons = events.Buttons(self.display)
        # self.proximity_sensors = self.robot.ProximitySensors()
        # self.rgb_leds = self.robot.RGBLEDs()
        # self.rgb_leds.set_brightness(2)
        # self.checkEvents.angular_event.calibrate(self.display)
        #
        # self.show_pressed = False
        #
        # self.buffer = ""
        #
        # self.timeout = 100
        # self.state = "init"
        # return
        pass

    def do_fsm(self):
        # loop_count: str = ''
        # display_details: str = 'line'
        #
        # while self.checkEvents.not_halted and self.stateActions.not_halted:
        #     # self.display.fill(0)
        #     self.checkEvents.check_events()
        #     triggered_event = self.checkEvents.triggered_event(self.stateMatrix[self.state])
        #     # print(f'{triggered_event=}')
        #
        #     next_state = self.stateMatrix[self.state].get(triggered_event, None)
        #     if next_state is not None:
        #         self.display.fill(0)
        #         self.state = next_state
        #         self.stateActions.do_actions(self.state)
        #         # time.sleep(state_delay)
        #
        #     line_scale = 24 / 1023
        #     prox_scale = 10
        #     # print(f'line: {self.checkEvents.lineEvents.line}')
        #
        #     if display_details == 'line':
        #             self.display.fill_rect(24, 64 - int(self.checkEvents.lineEvents.line[0] * line_scale), 8, int(self.checkEvents.lineEvents.line[0] * line_scale), 1)
        #             self.display.fill_rect(36, 64 - int(self.checkEvents.lineEvents.line[1] * line_scale), 8, int(self.checkEvents.lineEvents.line[1] * line_scale), 1)
        #             self.display.fill_rect(48, 64 - int(self.checkEvents.lineEvents.line[2] * line_scale), 8, int(self.checkEvents.lineEvents.line[2] * line_scale), 2)
        #             self.display.fill_rect(62, 64 - int(self.checkEvents.lineEvents.line[3] * line_scale), 8, int(self.checkEvents.lineEvents.line[3] * line_scale), 2)
        #             self.display.fill_rect(74, 64 - int(self.checkEvents.lineEvents.line[4] * line_scale), 8, int(self.checkEvents.lineEvents.line[4] * line_scale), 1)
        #             # self.display.fill_rect(86, 64 - int(self.checkEvents.lineEvents.line[0] * line_scale), 8, int(self.checkEvents.lineEvents.line[0] * line_scale), 1)
        #     if display_details == "prox":
        #             self.display.fill_rect(24, 64 - int(self.checkEvents.proximity_sensors.sensors['left_left'][1] * prox_scale), 8, int(self.checkEvents.proximity_sensors.sensors['left_left'][1] * prox_scale), 1)
        #             self.display.fill_rect(36, 64 - int(self.checkEvents.proximity_sensors.sensors['left_right'][1] * prox_scale), 8, int(self.checkEvents.proximity_sensors.sensors['left_right'][1] * prox_scale), 1)
        #             self.display.fill_rect(48, 64 - int(self.checkEvents.proximity_sensors.sensors['front_left'][1] * prox_scale), 8, int(self.checkEvents.proximity_sensors.sensors['front_left'][1] * prox_scale), 2)
        #             self.display.fill_rect(62, 64 - int(self.checkEvents.proximity_sensors.sensors['front_right'][1] * prox_scale), 8, int(self.checkEvents.proximity_sensors.sensors['front_right'][1] * prox_scale), 2)
        #             self.display.fill_rect(74, 64 - int(self.checkEvents.proximity_sensors.sensors['right_left'][1] * prox_scale), 8, int(self.checkEvents.proximity_sensors.sensors['right_left'][1] * prox_scale), 1)
        #             self.display.fill_rect(86, 64 - int(self.checkEvents.proximity_sensors.sensors['front_right'][1] * prox_scale), 8, int(self.checkEvents.proximity_sensors.sensors['right_right'][1] * prox_scale), 1)
        #
        #     self.display.text(f"s:{self.state}", 0, 0)
        #     if len(loop_count) > 20:
        #         loop_count = ''
        #     self.display.show()
        #     actions.rgb_leds.show()
        #     if clock_rate > 0:
        #         time.sleep(clock_rate)
        #     # else:
        #     #     input(f"{state}, step")
        pass
