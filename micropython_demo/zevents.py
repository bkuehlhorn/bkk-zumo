
import time
from zumo_2040_robot import robot
import button

from ucollections import deque


class Buttons(object):
    def __init__(self, display):
        self.display = display
        self.button_a = button.ButtonA()
        self.button_a.debounce_ms = 500
        self.button_a.long_press_ms = 7500
        self.button_b = button.ButtonB()
        self.button_b.debounce_ms = 500
        self.button_b.long_press_ms = 7500
        self.button_c = button.ButtonC()
        self.buttons = [button.ButtonA(), button.ButtonB(), button.ButtonC()]
        self.buttons_release()
        self.buttons_pressed = deque((), 10)
        # self.button_a_released = True
        # self.button_b_released = True
        # self.button_c_released = True
        self.buttons_list = [False, False, False]

    def buttons_release(self):
        for button_set in self.buttons:
            button_set.debounce_ms = 500
            button_set.long_press_ms = 7500

    def clear_buttons(self):
        self.buttons_pressed = deque((), 10)

    def check_button_pressed(self) -> list:
        # if self.button_a.is_pressed():
        #     if not self.buttons_list[0]:
        button_labels = 'abc'

        for button_index in range(len(self.buttons_list)):
            # self.display.text(f'pressed: {button_index}', 0, 14)
            if self.buttons[button_index].is_pressed() and not self.buttons_list[button_index]:
                self.buttons_list[button_index] = True
                if self.buttons[button_index].check():
                    self.display.text(f'bp:{button_labels[button_index]}', 0, 14)
                    self.buttons_pressed.append(button_labels[button_index])
            elif not self.buttons[button_index].is_pressed():
                self.buttons_list[button_index] = False
        return self.buttons_list

    def get_button_pressed(self) -> str:
        if len(self.buttons_pressed) > 0:
            return f'event_{self.buttons_pressed.popleft()}'
        else:
            return ''

    def is_pressed(self) -> list:
        # self.button_a.check()
        # return ['1','2','3']
        return [self.button_a.is_pressed(),
               self.button_b.is_pressed(),
               self.button_c.is_pressed()]


max_timeout = 500
min_timeout = 1
class CheckEvents(object):
    def __init__(self, events, _timer, _display):
        self.display = _display
        self.events = events
        self.not_halted = True
        self.triggered = False
        self.not_triggered = True
        self.log = []
        self.timer = _timer
        self.buttons = Buttons(_display)

    def triggered_event(self) -> str:
        button_event_list = self.buttons.check_button_pressed()
        button_event = self.buttons.get_button_pressed()
        if self.timer.event():
            return "timeout_triggered"
        if button_event is not None:
            self.display.text(f'be:{button_event}', 0, 14)
            return f'button_{button_event}'
        return None


def prompt_event(_state, _events) -> bool:
    text = input(f"Event:")
    return False

# def button_event(_state, _events) -> str:
#     """
#     Check button a, b, c
#     Return button_{button}_event if button {button} is pressed
#     Return None if no button is pressed
#     """
#     # button.
#     return None

def proximity_event(_state, _events) -> str:
    """
    Check if proximity return is different from current/init value
    Return closer_{detector} if greater
    Return farther_{detector} if less
    Return None if unchanged
    """
    return ""

    # Read the proximity sensors.
    # proximity_sensors.read()
    # reading_left = proximity_sensors.left_counts_with_left_leds()
    # reading_front_left = proximity_sensors.front_counts_with_left_leds()
    # reading_front_right = proximity_sensors.front_counts_with_right_leds()
    # reading_right = proximity_sensors.right_counts_with_right_leds()
