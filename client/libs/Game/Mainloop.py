from threading import Thread
from time import time



class Mainloop():
    def __init__(self, period, onStartFunc, onLoopFunc, onEndFunc, after, cancel):
        self.period = period
        self.after = after
        self.cancel = cancel
        self.afterId = None

        self.debugTime = 0

        self.onStartFunc = onStartFunc
        self.onLoopFunc = onLoopFunc
        self.onEndFunc = onEndFunc

    def start(self):
        self.onStartFunc()
        self.loop()

    def end(self):
        if self.afterId != None:
            self.cancel(self.afterId)

            self.onEndFunc()

    def loop(self):
        newDebugTime = int(round(time() * 1000))
        print(newDebugTime-self.debugTime)
        self.debugTime = newDebugTime

        self.onLoopFunc()
        self.afterId = self.after(self.period, self.loop)
