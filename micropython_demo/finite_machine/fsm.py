# This example shows how to read the three buttons on the Pololu Zumo 2040
# Robot.  It configures button A with an unusually high debounce time of
# 500 ms so you can see the debouncing effect by pressing the button
# quickly.

import time
from finite_machine import actions
from finite_machine import events


frame_speed = 1
max_timeout = 5
min_timeout = 1
clock_rate = 0
state_delay = 1

class FSM():
    def __init__(self, _checkEvents, _stateActions, _stateMatrix, _robot, _display):
        # logging = fsm_logging()
        self.checkEvents = _checkEvents
        # FSM => matrix[state, event] of nextState
        self.stateActions = _stateActions
        self.stateMatrix = _stateMatrix
        self.robot = _robot
        self.display = _display
        self.buttons = events.Buttons(self.display)
        self.proximity_sensors = self.robot.ProximitySensors()
        self.rgb_leds = self.robot.RGBLEDs()
        self.rgb_leds.set_brightness(2)
        self.checkEvents.angular_event.calibrate(self.display)
        self.imu = self.robot.IMU()
        self.imu.reset()
        self.imu.enable_default()

        self.show_pressed = False

        self.buffer = ""

        self.timeout = 100
        self.state = "init"
        return

    def do_fsm(self, _display_details = 'line'):
        loop_count: str = ''
        display_details: str = _display_details
        update_count = 0
        update_count_start = 1
        self.display.fill(0)

        while self.checkEvents.not_halted and self.stateActions.not_halted:
            # self.display.fill(0)
            self.checkEvents.check_events()
            triggered_event = self.checkEvents.triggered_event(self.stateMatrix[self.state])
            # print(f'{self.stateMatrix[self.state].keys()=}')

            next_state = self.stateMatrix[self.state].get(triggered_event, None)
            if next_state is not None and next_state != self.state:
                self.display.fill(0)
                update_count = 0
                self.state = next_state
                self.stateActions.do_actions(self.state)
                # time.sleep(state_delay)

            line_scale = 24 / 1023
            prox_scale = 10
            # print(f'{self.state=}\n{self.checkEvents.lineEvents.line}')

            if display_details == 'line':
                self.display.fill_rect(24, 64 - int(self.checkEvents.lineEvents.line[0] * line_scale), 8, int(self.checkEvents.lineEvents.line[0] * line_scale), 1)
                self.display.fill_rect(36, 64 - int(self.checkEvents.lineEvents.line[1] * line_scale), 8, int(self.checkEvents.lineEvents.line[1] * line_scale), 1)
                self.display.fill_rect(48, 64 - int(self.checkEvents.lineEvents.line[2] * line_scale), 8, int(self.checkEvents.lineEvents.line[2] * line_scale), 2)
                self.display.fill_rect(62, 64 - int(self.checkEvents.lineEvents.line[3] * line_scale), 8, int(self.checkEvents.lineEvents.line[3] * line_scale), 2)
                self.display.fill_rect(74, 64 - int(self.checkEvents.lineEvents.line[4] * line_scale), 8, int(self.checkEvents.lineEvents.line[4] * line_scale), 1)
                # self.display.fill_rect(86, 64 - int(self.checkEvents.lineEvents.line[0] * line_scale), 8, int(self.checkEvents.lineEvents.line[0] * line_scale), 1)
                update_count = update_count_start
            elif display_details == 'line_display' and update_count == 0:
                self.display.fill_rect(0, 12, 128, 24, 0)
                self.display.text(str(self.checkEvents.lineEvents.line[0]), 0, 12)
                self.display.text(str(self.checkEvents.lineEvents.line[1]), 35, 12)
                self.display.text(str(self.checkEvents.lineEvents.line[2]), 70, 12)
                self.display.text(str(self.checkEvents.lineEvents.line[3]), 0, 24)
                self.display.text(str(self.checkEvents.lineEvents.line[4]), 35, 24)
                update_count = update_count_start
            elif display_details == "prox":
                self.display.fill_rect(24, 64 - int(self.checkEvents.proximity_sensors.sensors['left_left'][1] * prox_scale), 8, int(self.checkEvents.proximity_sensors.sensors['left_left'][1] * prox_scale), 1)
                self.display.fill_rect(36, 64 - int(self.checkEvents.proximity_sensors.sensors['left_right'][1] * prox_scale), 8, int(self.checkEvents.proximity_sensors.sensors['left_right'][1] * prox_scale), 1)
                self.display.fill_rect(48, 64 - int(self.checkEvents.proximity_sensors.sensors['front_left'][1] * prox_scale), 8, int(self.checkEvents.proximity_sensors.sensors['front_left'][1] * prox_scale), 2)
                self.display.fill_rect(62, 64 - int(self.checkEvents.proximity_sensors.sensors['front_right'][1] * prox_scale), 8, int(self.checkEvents.proximity_sensors.sensors['front_right'][1] * prox_scale), 2)
                self.display.fill_rect(74, 64 - int(self.checkEvents.proximity_sensors.sensors['right_left'][1] * prox_scale), 8, int(self.checkEvents.proximity_sensors.sensors['right_left'][1] * prox_scale), 1)
                self.display.fill_rect(86, 64 - int(self.checkEvents.proximity_sensors.sensors['right_right'][1] * prox_scale), 8, int(self.checkEvents.proximity_sensors.sensors['right_right'][1] * prox_scale), 1)
                update_count = update_count_start
            elif display_details == 'prox_display' and update_count == 0:
                self.display.fill_rect(0, 12, 128, 24, 0)
                self.display.text(str(self.checkEvents.proximity_sensors.sensors['left_left'][1]), 0, 12)
                self.display.text(str(self.checkEvents.proximity_sensors.sensors['front_left'][1]), 35, 12)
                self.display.text(str(self.checkEvents.proximity_sensors.sensors['front_left'][1]), 70, 12)
                self.display.text(str(self.checkEvents.proximity_sensors.sensors['front_right'][1]), 0, 24)
                self.display.text(str(self.checkEvents.proximity_sensors.sensors['front_right'][1]), 35, 24)
                self.display.text(str(self.checkEvents.proximity_sensors.sensors['right_right'][1]), 70, 24)
                update_count = update_count_start
            elif display_details == 'imu_display' and update_count == 0:
                self.imu.read()
                g = self.imu.gyro.last_reading_dps
                a = self.imu.acc.last_reading_g
                m = self.imu.mag.last_reading_gauss
                self.display.text("gyro (dps):   <B", 0, 8)
                # self.display.text("{:>5.1f} {:>5.1f}{:>5.1f}".format(*g), 0, 18)
                self.display.text(f"{g[0]},{g[1]},{g[2]}", 0, 18)
                self.display.text("acc (g):", 0, 27)
                # self.display.text("{:>5.2f} {:>5.2f}{:>5.2f}".format(*a), 0, 37)
                self.display.text(f"{a[0]},{a[1]},{a[2]}", 0, 37)
                self.display.text("mag (gauss):", 0, 47)
                # self.display.text("{:>5.2f} {:>5.2f}{:>5.2f}".format(*m), 0, 57)
                self.display.text(f"{m[0]:.2f},{m[1]:.2f},{m[2]:.2f}", 0, 57)
            update_count -= 1
            if update_count == update_count_start//2 | update_count_start % 2 == 0:
                self.display.text(str(update_count), 0, 36)

            self.display.text(f"s:{self.state}, {display_details}", 0, 0)
            if len(loop_count) > 20:
                loop_count = ''
            self.display.show()
            actions.rgb_leds.show()
            if clock_rate > 0:
                time.sleep(clock_rate)
            # else:
            #     input(f"{state}, step")

