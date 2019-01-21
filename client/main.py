import time
import tkinter
import random

from libs.Game.GameClient import GameClient
from libs.Game.Mainloop import Mainloop



class SnakeStyle():
    def __init__(self, color, headColor):
        self.color = color
        self.headColor = headColor

class SnakeStyleX():
    def __init__(self, playerSnakeStyle, remoteSnakeStyle):
        self.playerSnakeStyle = playerSnakeStyle
        self.remoteSnakeStyle = remoteSnakeStyle

class Player():
    def __init__(self, game, id, blocks, style):
        self.game = game
        self.id = id

        self.blocks = blocks.copy()
        self.style = style

    def update(self):
        pass

    def draw(self):
        scaleX = self.game.map.scale[0]
        scaleY = self.game.map.scale[1]

        for block in self.blocks:
            x = block['x']*scaleX
            y = block['y']*scaleY
            xSize = scaleX
            ySize = scaleY

            if block['isHead']:
                color = self.style.headColor

                self.game.canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)
                self.game.canvas.create_text(x+xSize/2, y+ySize/2, text=self.id, fill='#FFFFFF')
            else:
                color = self.style.color

                self.game.canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)

    def fromDict(game, playerDict):
        styleX = snakeStyles[playerDict['snake']['style']]
        if playerDict['isPlayer']:
            style = styleX.playerSnakeStyle
        else:
            style = styleX.remoteSnakeStyle

        return Player(game, playerDict['id'], playerDict['snake']['blocks'], style)

class GameMap():
    def __init__(self, size, scale):
        self.size = size.copy()
        self.scale = scale.copy()

    def fromDict(gameDict):
        size = [gameDict['xSize'], gameDict['ySize']]
        scale = [gameDict['xScale'], gameDict['yScale']]

        return GameMap(size, scale)

    def getScreenSize(self):
        return list(map(lambda zip_: zip_[0]*zip_[1], zip(self.size, self.scale)))

class Game():
    def __init__(self, gameClient):
        self.gameClient = gameClient

        initInfoMessage = self.gameClient.communicate('initInfo', {})
        self.map = GameMap.fromDict(initInfoMessage['gameMap'])
        screenSize = self.map.getScreenSize()

        self.root = tkinter.Tk()
        self.root.geometry('{width}x{height}'.format(width=screenSize[0], height=screenSize[1]))
        self.root.protocol('WM_DELETE_WINDOW', self.end)

        self.canvas = tkinter.Canvas(self.root, width=screenSize[0], height=screenSize[1], bg='#FFFFFF', highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind_all('<Key>', self.keyPressed)

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
            players.append(Player.fromDict(self, playerDict))

        objects = [self]
        objects.extend(players)

        return objects

    def update(self):
        self.canvas.delete('all')

    def draw(self):
        pass

    def end(self):
        self.gameClient.communicate('end', {})

        self.gameClient.end()

        self.root.destroy()

    def keyPressed(self, event):
        vel = None
        key = event.keysym

        if key == 'Up':
            vel = [0, -1]
        elif key == 'Down':
            vel = [0, 1]
        elif key == 'Left':
            vel = [-1, 0]
        elif key == 'Right':
            vel = [1, 0]

        if vel != None:
            message = {
                'vel': {
                    'x': vel[0],
                    'y': vel[1],
                },
            }

            changeXYMessage = self.gameClient.communicate('changeVel', message)



snakeStyles = {
    'style1': SnakeStyleX(SnakeStyle('#FF0000', '#000000'), SnakeStyle('#990000', '#222222'))
}



def main():
    import sys

    gameClient = GameClient('192.168.1.4', 4041, True)
    gameClient.begin()

    try:
        game = Game(gameClient)
    except Exception as e:
        gameClient.end()

        raise e



if __name__ == '__main__':
    main()
