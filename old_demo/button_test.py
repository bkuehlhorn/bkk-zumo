# This example shows how to read the three buttons on the Pololu Zumo 2040
# Robot.  It configures button A with an unusually high debounce time of
# 500 ms so you can see the debouncing effect by pressing the button
# quickly.

from zumo_2040_robot import robot
import button

from ucollections import deque

buffer_len = 15

class Buttons(object):
    def __init__(self, _display):
        self.display = _display
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
            if self.buttons[button_index].is_pressed() and not self.buttons_list[button_index]:
                self.buttons_list[button_index] = True
                if self.buttons[button_index].check():
                    self.buttons_pressed.append(button_labels[button_index])
            elif not self.buttons[button_index].is_pressed():
                self.buttons_list[button_index] = False
        return self.buttons_list

    def get_button_pressed(self) -> str:
        if len(self.buttons_pressed) > 0:
            return self.buttons_pressed.popleft()
        else:
            return ''

    def is_pressed(self) -> list:
        # self.button_a.check()
        # return ['1','2','3']
        return [self.button_a.is_pressed(),
               self.button_b.is_pressed(),
               self.button_c.is_pressed()]


display = robot.Display()
buttons = Buttons(display)
proximity_sensors = robot.ProximitySensors()
rgb_leds = robot.RGBLEDs()
rgb_leds.set_brightness(2)

show_pressed = False

buffer = ""

while True:
    display.fill(0)

    # Read the proximity sensors.
    proximity_sensors.read()
    reading_left = proximity_sensors.left_counts_with_left_leds()
    reading_front_left = proximity_sensors.front_counts_with_left_leds()
    reading_front_right = proximity_sensors.front_counts_with_right_leds()
    reading_right = proximity_sensors.right_counts_with_right_leds()

    is_pressed = buttons.check_button_pressed()
    display.text("A:" + str(is_pressed[0])+':'+str(buttons.button_a.not_pressed_t), 0, 0)
    display.text("B:" + str(is_pressed[1])+':'+str(buttons.button_b.not_pressed_t), 0, 8)
    display.text("C:" + str(is_pressed[2])+':'+str(buttons.button_c.not_pressed_t), 0, 16)

    buffer += buttons.get_button_pressed()
    if len(buffer) > buffer_len:
        buffer = ''

    # if show_pressed:
    #     buffer += buttons.get_button_pressed()
    #     if len(buttons.buttons_pressed) == 0:
    #         show_pressed = False
    # elif len(buttons.buttons_pressed) > 4:
    #     show_pressed = True

    buffer += buttons.get_button_pressed()

    display.text("r="+str(reading_right)+':'+str(reading_front_right), 0, 28)
    display.text("l="+str(reading_left)+':'+str(reading_front_left), 0, 36)
    display.text("A:"+str(buttons.button_a.last_event_t), 0, 44)
    # display.text(str(len(buttons.buttons_pressed)), 0, 56)
    display.text(buffer, 0, 56)

    display.show()
