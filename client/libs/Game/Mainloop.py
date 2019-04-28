from time import time



class Mainloop():
    def __init__(self, period, onStartFunc, onLoopFunc, onEndFunc, after, cancel):
        self.period = period
        self.after = after
        self.cancel = cancel

        self.afterId = None
        self.running = False

        self.debugTime = 0
        self.statsPeriod = None

        self.onStartFunc = onStartFunc
        self.onLoopFunc = onLoopFunc
        self.onEndFunc = onEndFunc

    def start(self):
        self.running = True
        self.onStartFunc()

        if self.running:
            self.loop()

    def end(self):
        self.running = False
        
        if self.afterId != None:
            self.cancel(self.afterId)

            self.onEndFunc()

    def getStats(self):
        period = self.statsPeriod
        fps = 1000/period
        eff = (2*self.period-period)/self.period

        stats = {
            'period': self.statsPeriod,
            'fps': 1000/self.statsPeriod,
            'eff': eff,
        }

        return stats

    def loop(self):
        if self.running:
            newDebugTime = int(round(time() * 1000))
            self.statsPeriod = newDebugTime-self.debugTime
            self.debugTime = newDebugTime

            self.onLoopFunc()
            self.afterId = self.after(self.period, self.loop)
