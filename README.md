# ZUMO Finite State Machine

## Summary


FSM consists of *self.stateMatrix* and *self.actionMatrix*

### stateMatrix
Dictionary of States.
Each State is a list of tuples of event and next state

Events are entries in *events.Event_trigger*
### actionMatrix
Dictionary of actions for each state
Actions are list of tuples of action method, parameters