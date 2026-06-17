import graphviz
import os

from analyze_fsm import actions, events, proximity_sensors_event

led_seconds = 5000 # micro ticks
timer_action_event = events.Timer()

robot = 'xx'
display = 'robot.Display()'
lineSensors = 'robot.LineSensors()'
proximity_sensors = 'proximity_sensors_event.ProximitySensors(robot)'
angular_event = 'events.AngularEvent(robot)'

print(f'{os.listdir()}')
fsm_folders_os = os.listdir()
# fsm_folders_os = os.listdir('micropython_demo/fsm_files')
# fsm_folders = ['button_fsm', 'led_fsm', 'motor_fsm', 'motor_fb_fsm',
#                'proximity_fsm', 'line_following_fsm',]
# fsm_files = fsm_folders[5]
for fsm_file in fsm_folders_os:
    s = fsm_file.split('.')
    if len(s) > 1 and s[1] == 'py':
        print(f'{fsm_file}, {s=}')
        match s[0]:
            case 'button_fsm': from micropython_demo.fsm_files import button_fsm as fsm_import
            case 'led_fsm': from micropython_demo.fsm_files import led_fsm as fsm_import
            case 'motor_fsm': from micropython_demo.fsm_files import motor_fsm as fsm_import
            case 'motor_fb_fsm': from micropython_demo.fsm_files import motor_fb_fsm as fsm_import
            case 'proximity_fsm': from micropython_demo.fsm_files import proximity_fsm as fsm_import
            case 'line_following_fsm': from micropython_demo.fsm_files import line_following_fsm as fsm_import
            case 'edge_avoid_fsm': from micropython_demo.fsm_files import edge_avoid_fsm as fsm_import

        fsm_machine = fsm_import.FSM(events, actions, display, proximity_sensors, angular_event, timer_action_event, lineSensors,
                                     proximity_sensors_event)
        fsm_machine.stateMatrix.keys()
        checkEvents = events.CheckEvents(fsm_machine.stateMatrix, timer_action_event,
                                         display, lineSensors, proximity_sensors, angular_event)
        stateActions = actions.StateAction(fsm_machine.actionMatrix, display)

        stateMatrix = dict()
        edges = set()
        stateMatrixKeys = list(fsm_machine.stateMatrix.keys())
        for key in fsm_machine.stateMatrix.keys():
            stateMatrix[key] = dict()
            for trigger, edge in fsm_machine.stateMatrix[key].items():
                stateMatrix[key][trigger] = edge
                edges.add(edge)


        missing_states = set(fsm_machine.stateMatrix.keys()) - set(fsm_machine.actionMatrix.keys())
        missing_actions = set(fsm_machine.actionMatrix.keys()) - set(fsm_machine.stateMatrix.keys())
        missing_edges = edges - set(stateMatrixKeys)

        print(f'{missing_states=}')
        print(f'{missing_actions=}')
        # print(f'{stateMatrixKeys=}')
        # print(f'{stateMatrix=}')
        print(f'{missing_edges=}\n\n')

        dot = graphviz.Digraph(comment=f'{fsm_file} FSM')
        for key in stateMatrix.keys():
            dot.node(key)
        for key in stateMatrix.keys():
            for trigger, edge in stateMatrix[key].items():
                dot.edge(key, edge, label=trigger)
                # if key in ['init', 'done'] or edge in ['init', 'done']:
                #     dot.edge(key, edge, label=trigger)
                #     pass
                # else:
                #     if trigger not in ['button_a_triggered',
                #                        'button_b_triggered',
                #                        'button_c_triggered']:
                #         dot.edge(key, edge, label=trigger)

        u = dot.unflatten(stagger=150)
        dot.render(filename=fsm_file, view=True, format='png', directory='diagrams')
        u.view()
