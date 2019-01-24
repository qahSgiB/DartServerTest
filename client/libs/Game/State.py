from .Mainloop import Mainloop



class State():
    def __init__(self, name, period, onStartFunc, onLoopFunc, onEndFunc, onEvents, after, cancel):
        self.name = name
        self.mainloop = Mainloop(period, onStartFunc, onLoopFunc, onEndFunc, after, cancel)
        self.onEvents = onEvents

    def start(self):
        self.mainloop.start()

    def end(self):
        self.mainloop.end()

    def event(self, eventName, eventDetails):
        self.onEvents.get(eventName, lambda eventDetails: 0)(eventDetails)

class StateManager():
    def __init__(self, after, cancel, period=50):
        self.after = after
        self.cancel = cancel
        self.period = period

        self.states = {}
        self.runningState = None

    def event(self, eventName, eventDetails):
        if self.runningState != None:
            self.states[self.runningState].event(eventName, eventDetails)

    def addState(self, name, onStartFunc, onLoopFunc, onEndFunc, onEvents, period=None):
        period = self.period if period == None else period

        self.states[name] = State(name, period, onStartFunc, onLoopFunc, onEndFunc, onEvents, self.after, self.cancel)

    def startState(self, state):
        self.runningState = state
        self.states[self.runningState].start()

    def endState(self):
        if self.runningState != None:
            self.states[self.runningState].end()
            self.runningState = None

    def setState(self, state):
        self.endState()
        self.startState(state)
