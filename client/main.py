import time
import tkinter
import random

from libs.Game.GameClient import GameClient
from libs.Game.Mainloop import Mainloop


class PlayerRemoteX():
    def __init__(self, ifPlayer, ifRemote):
        self.ifPlayer = ifPlayer
        self.ifRemote = ifRemote

    def get(self, isPlayer):
        return self.ifPlayer if isPlayer else self.ifRemote

class SnakeStyle():
    def __init__(self, draw):
        self.draw = draw

    def stylePlayer1Draw(snake):
        canvas = snake.game.canvas
        gameMap = snake.game.map

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        for block in snake.blocks:
            x = block.pos[0]*scaleX
            y = block.pos[1]*scaleY
            xSize = scaleX
            ySize = scaleY

            if block.isHead:
                color = '#FF0000'
            else:
                color = '#000000'

            canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)

    def styleRemote1Draw(snake):
        canvas = snake.game.canvas
        gameMap = snake.game.map

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        for block in snake.blocks:
            x = block.pos[0]*scaleX
            y = block.pos[1]*scaleY
            xSize = scaleX
            ySize = scaleY

            if block.isHead:
                color = '#996666'
            else:
                color = '#666666'

            canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)

class Block():
    def __init__(self, pos, isHead):
        self.pos = pos.copy()
        self.isHead = isHead

    def fromDict(blockDict):
        return Block([blockDict['x'], blockDict['y']], blockDict['isHead'])

class Snake():
    def __init__(self, game, blocks, style):
        self.game = game
        self.blocks = blocks
        self.style = style

    def draw(self):
        self.style.draw(self)

    def fromDict(snakeDict, game, isPlayer=False):
        return Snake(game, [Block.fromDict(blockDict) for blockDict in snakeDict['blocks']], snakeStyles[snakeDict['style']].get(isPlayer))

class Player():
    def __init__(self, game, id, snake):
        self.game = game
        self.id = id

        self.snake = snake

    def draw(self):
        self.snake.draw()

    def fromDict(playerDict, game):
        isPlayer = playerDict['isPlayer']

        return Player(game, playerDict['id'], Snake.fromDict(playerDict['snake'], game, isPlayer))

class GameMap():
    def __init__(self, size, scale):
        self.size = size.copy()
        self.scale = scale.copy()

    def fromDict(gameDict, screenSize):
        size = [gameDict['xSize'], gameDict['ySize']]
        scale = list(map(lambda zip_: zip_[0]/zip_[1], zip(screenSize, size)))

        return GameMap(size, scale)

    def getScreenSize(self):
        return list(map(lambda zip_: int(zip_[0]*zip_[1]), zip(self.size, self.scale)))

class Game():
    def __init__(self, screenSize, gameServerAddress, gameServerPort):
        self.gameServerAddress = gameServerAddress
        self.gameServerPort = gameServerPort
        self.gameClient = None

        self.screenSize = screenSize.copy()

        self.root = tkinter.Tk()
        self.root.geometry('{width}x{height}'.format(width=self.screenSize[0], height=self.screenSize[1]))
        self.root.protocol('WM_DELETE_WINDOW', self.end)
        self.root.title('Snako pythonish client')

        self.canvas = tkinter.Canvas(self.root, width=self.screenSize[0], height=self.screenSize[1], bg='#FFFFFF', highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind_all('<Key>', self.keyPressed)

        self.mainloop = Mainloop(50, self.gameStateOnStart, self.gameStateOnLoop, self.gameStateOnEnd, self.root.after, self.root.after_cancel)
        self.mainloop.start()

        self.root.mainloop()

    def gameStateOnStart(self):
        self.gameClient = GameClient(self.gameServerAddress, self.gameServerPort, True)
        self.gameClient.begin()

        initInfoMessage = self.gameClient.communicate('initInfo', {})
        error = initInfoMessage['error']

        if len(error) == 0:
            self.map = GameMap.fromDict(initInfoMessage['gameMap'], self.screenSize)

            addPlayerMessage = self.gameClient.communicate('addPlayer', {})

            self.playerId = addPlayerMessage['player']['id']
        else:
            if error['title'] == 'GameFull':
                self.gameClient.output('Game is full.\nTry connecting later.')
                self.gameClient.end()

    def gameStateOnLoop(self):
        self.canvas.delete('all')

        playersDict = self.gameClient.communicate('loop', {})['players']
        players = []

        for playerDict in playersDict:
            players.append(Player.fromDict(playerDict, self))

        for player in players:
            player.draw()

    def gameStateOnEnd(self):
        self.gameClient.communicate('end', {})
        self.gameClient.end()

    def end(self):
        self.mainloop.end()
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
    'style1': PlayerRemoteX(SnakeStyle(SnakeStyle.stylePlayer1Draw), SnakeStyle(SnakeStyle.styleRemote1Draw))
}



def main():
    serverAddress = '192.168.1.4'
    serverPort = 4042

    game = Game([400, 400], serverAddress, serverPort)



if __name__ == '__main__':
    main()
