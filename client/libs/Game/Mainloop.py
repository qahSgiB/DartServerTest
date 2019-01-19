class Mainloop():
    def __init__(self, after, period, getObjects):
        self.after = after
        self.period = period
        self.getObjects = getObjects

    def start(self):
        self.loop()

    def loop(self):
        for object in self.getObjects():
            object.update()
            object.draw()

        self.after(self.period, self.loop)
