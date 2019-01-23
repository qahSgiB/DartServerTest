class State():
    def __init__(self, name, init, getObjects, after, cancel, delay=50):
        self.name = name
        self.init = init
        self.mainloop = Mainloop(after, delay, getObjects, cancel)

    def start(self):
        self.init()
        self.mainloop.start()

    def stop():
        self.mainloop.stop()

class StateManager():
    def __init__(self, after, cancel, delay):
        self.after = after
        self.cancel = cancel
        self.states = {}

    def addState(self, name, init, getObjects, delay=50):
        self.states[name] = State(name, )
