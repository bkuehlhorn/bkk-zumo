"""
FSM to test button and 6 leds
"""
from zumo_2040_robot import robot

from finite_machine import fsm
from finite_machine import actions
from finite_machine import events
from finite_machine import proximity_sensors_event

display = robot.Display()
lineSensors = robot.LineSensors()
proximity_sensors = proximity_sensors_event.ProximitySensors(robot)
angular_event = events.AngularEvent(robot)

led_seconds = 5000 # micro ticks
timer_action_event = events.Timer()
fsm_file = 'edge_avoid_fsm'
if fsm_file == "button_fsm": from fsm_files import button_fsm as fsm_import
elif fsm_file == "led_fsm": from fsm_files import led_fsm as fsm_import
elif fsm_file == "motor_fsm": from fsm_files import motor_fsm as fsm_import
elif fsm_file == "motor_fb_fsm": from fsm_files import motor_fb_fsm as fsm_import
elif fsm_file == "proximity_fsm": from fsm_files import proximity_fsm as fsm_import
elif fsm_file == "line_following_fsm": from fsm_files import line_following_fsm as fsm_import
elif fsm_file == "edge_avoid_fsm": from fsm_files import edge_avoid_fsm as fsm_import
fsm_machine = fsm_import.FSM(events, actions, display, proximity_sensors, angular_event, timer_action_event, lineSensors, proximity_sensors_event)

print(fsm_file)
# checkEvents = events.CheckEvents(fsm_machine.stateMatrix, timer_action_event,
#                                  display, lineSensors, proximity_sensors, angular_event)
stateActions = actions.StateAction(fsm_machine.actionMatrix, display)

fsm = fsm.FSM(fsm_machine, stateActions, robot, display, fsm_file)
fsm.do_fsm(fsm_machine.display_details)
print("done")
