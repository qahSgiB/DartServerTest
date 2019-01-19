import time
import tkinter
import random

from libs.Game.GameClient import GameClient
from libs.Game.Mainloop import Mainloop



class Player():
    def __init__(self, game, pos, id, color):
        self.game = game
        self.color = color

        self.id = id

        self.pos = pos.copy()
        self.r = 25

    def setPos(self, newPos):
        self.pos = newPos.copy()

    def update(self):
        pass

    def draw(self):
        self.game.canvas.create_oval(self.pos[0]-self.r, self.pos[1]-self.r, self.pos[0]+self.r, self.pos[1]+self.r, fill=self.color, outline=self.color)
        self.game.canvas.create_text(self.pos[0], self.pos[1], text=self.id, fill='#000000')

class Game():
    def __init__(self, gameClient):
        self.gameClient = gameClient

        initInfoMessage = self.gameClient.communicate('initInfo', {})
        self.size = [initInfoMessage['width'], initInfoMessage['height']]

        self.root = tkinter.Tk()
        self.root.geometry('{width}x{height}'.format(width=self.size[0], height=self.size[1]))
        self.root.protocol('WM_DELETE_WINDOW', self.end)

        self.canvas = tkinter.Canvas(self.root, width=self.size[0], height=self.size[1], bg='#FFFFFF', highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.mousePressed)

        addPlayerMessage = self.gameClient.communicate('addPlayer', {})

        self.playerId = addPlayerMessage['player']['id']

        self.root.title('DartServerTest Client | id: {id}'.format(id=self.playerId))

        self.mainloop = Mainloop(self.root.after, 50, self.getObjects)

        self.mainloop.start()
        self.root.mainloop()

    def getObjects(self):
        playersDict = self.gameClient.communicate('loop', {})['players']
        players = []

        for playerDict in playersDict:
            color = '#0000FF' if playerDict['id'] == self.playerId else '#00FF00'
            pos = [playerDict['x'], playerDict['y']]
            players.append(Player(self, pos, playerDict['id'], color))

        objects = [self]
        objects.extend(players)

        return objects

    def update(self):
        self.canvas.delete('all')

    def draw(self):
        pass

    def end(self):
        self.gameClient.communicate('end', {})

        self.root.destroy()

    def mousePressed(self, event):
        x = event.x
        y = event.y

        message = {
            'x': x,
            'y': y,
        }

        changeXYMessage = self.gameClient.communicate('changeXY', message)





def test():
    gameClient = GameClient('192.168.1.4', 4040, True)
    gameClient.begin()

    game = Game(gameClient)



if __name__ == '__main__':
    test()
