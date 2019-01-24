import time
import tkinter
import random

from libs.Game.GameClient import GameClient
from libs.Game.Mainloop import Mainloop
from libs.Game.State import StateManager



class PlayerRemoteX():
    def __init__(self, ifPlayer, ifRemote):
        self.ifPlayer = ifPlayer
        self.ifRemote = ifRemote

    def get(self, isPlayer):
        return self.ifPlayer if isPlayer else self.ifRemote

class Style():
    def __init__(self, draw):
        self.draw = draw

    def styleSnakePlayer1Draw(snake, game):
        canvas = game.canvas
        gameMap = game.gameSMap

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

    def styleSnakeRemote1Draw(snake, game):
        canvas = game.canvas
        gameMap = game.gameSMap

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

    def styleMaze1Draw(maze, game):
        canvas = game.canvas
        gameMap = game.gameSMap

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        for block in maze.blocks:
            x = block.pos[0]*scaleX
            y = block.pos[1]*scaleY
            xSize = scaleX
            ySize = scaleY

            color = '#0000FF'

            canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)

class SnakeBlock():
    def __init__(self, pos, isHead):
        self.pos = pos.copy()
        self.isHead = isHead

    def fromDict(blockDict):
        return SnakeBlock([blockDict['x'], blockDict['y']], blockDict['isHead'])

class Snake():
    def __init__(self, blocks, style):
        self.blocks = blocks
        self.style = style

    def draw(self, game):
        self.style.draw(self, game)

    def fromDict(snakeDict, isPlayer=False):
        return Snake([SnakeBlock.fromDict(blockDict) for blockDict in snakeDict['blocks']], snakeStyles[snakeDict['style']].get(isPlayer))

class Player():
    def __init__(self, id, snake):
        self.id = id

        self.snake = snake

    def draw(self, game):
        self.snake.draw(game)

    def fromDict(playerDict):
        isPlayer = playerDict['isPlayer']

        return Player(playerDict['id'], Snake.fromDict(playerDict['snake'], isPlayer))

class MazeBlock():
    def __init__(self, pos):
        self.pos = pos.copy()

    def fromDict(mazeBlockDict):
        return MazeBlock([mazeBlockDict['x'], mazeBlockDict['y']])

class Maze():
    def __init__(self, blocks):
        self.blocks = blocks.copy()

    def fromDict(mazeDict):
        blocks = []

        for blockDict in mazeDict['blocks']:
            blocks.append(MazeBlock.fromDict(blockDict))

        return Maze(blocks)

    def draw(self, game):
        mazeStyles['style1'].draw(self, game)

class GameMap():
    def __init__(self, size, scale, maze):
        self.size = size.copy()
        self.scale = scale.copy()
        self.maze = maze

    def fromDict(gameMapDict, screenSize):
        size = [gameMapDict['xSize'], gameMapDict['ySize']]
        scale = list(map(lambda zip_: zip_[0]/zip_[1], zip(screenSize, size)))

        return GameMap(size, scale, Maze.fromDict(gameMapDict['maze']))

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
        self.canvas.bind_all('<Key>', lambda event: self.stateManager.event('keyPressed', event))

        self.stateManager = StateManager(self.canvas.after, self.canvas.after_cancel, 50)
        self.stateManager.addState('main', self.mainStateOnStart, self.mainStateOnLoop, self.mainStateOnEnd, {'keyPressed': self.mainStateOnKeyPressed})
        self.error = {}
        self.stateManager.addState('game', self.gameStateOnStart, self.gameStateOnLoop, self.gameStateOnEnd, {'keyPressed': self.gameStateOnKeyPressed})
        # self.stateManager.addState('gameSpectate', self.gameSpectateStateOnStart, self.gameSpectateStateOnLoop, self.gameSpectateStateOnEnd, {'keyPressed': self.gameSpectateStateOnKeyPressed})

        self.stateManager.setState('main')

        self.root.mainloop()

    def fontSize(self, fontSize):
        return int(fontSize*(min(self.screenSize[0], self.screenSize[1])/400))

    def end(self):
        self.stateManager.endState()
        self.root.destroy()

    # -------------------- state: game -------------------- #
    #
    # events: keyPressed
    #
    def gameStateOnKeyPressed(self, event):
        self.gameSStateManager.event('keyPressed', event)

    def gameStateOnStart(self):
        self.gameSGameClient = GameClient(self.gameServerAddress, self.gameServerPort, True)
        self.gameSGameClient.begin()

        self.gameSStateManager = StateManager(self.canvas.after, self.canvas.after_cancel, 50)
        self.gameSStateManager.addState('game.playing', self.gameSPlayingStateOnStart, self.gameSPlayingStateOnLoop, self.gameSPlayingStateOnEnd, {'keyPressed': self.gameSPlayingStateOnKeyPressed})
        self.gameSStateManager.addState('game.spectating', self.gameSSpectatingStateOnStart, self.gameSSpectatingStateOnLoop, self.gameSSpectatingStateOnEnd, {'keyPressed': self.gameSSpectatingStateOnKeyPressed})

        initInfoMessage = self.gameSGameClient.communicate('initInfo', {})
        self.gameSMap = GameMap.fromDict(initInfoMessage['gameMap'], self.screenSize)

        addPlayerMessage = self.gameSGameClient.communicate('addPlayer', {})
        self.gameSPlayerId = addPlayerMessage['player']['id']

        self.gameSStateManager.setState('game.spectating')

    def gameStateOnLoop(self):
        pass

    def gameStateOnEnd(self):
        self.gameSGameClient.communicate('end', {})
        self.gameSGameClient.end()

    # -------------------- state: game.spectating -------------------- #
    #
    # events: keyPressed
    #
    def gameSSpectatingStateOnKeyPressed(self, event):
        key = event.keysym

        if key == 'space':
            self.gameSStateManager.setState('game.playing')
        if key == 'q':
            self.gameSStateManager.endState()
            self.stateManager.setState('main')

    def gameSSpectatingStateOnStart(self):
        pass

    def gameSSpectatingStateOnLoop(self):
        self.canvas.delete('all')

        playersDict = self.gameSGameClient.communicate('spectate', {})['players']
        players = []

        for playerDict in playersDict:
            if playerDict['playing']:
                players.append(Player.fromDict(playerDict))

        for player in players:
            player.draw(self)

        self.gameSMap.maze.draw(self)

        screenSizeX = self.screenSize[0]
        screenSizeY = self.screenSize[1]
        fontSize = self.fontSize(8)

        self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(1/2)-fontSize*2, text='spectating'.format(address=self.gameServerAddress), font=('Purisa', fontSize))
        self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(1/2),            text='press <space> to start playing'.format(address=self.gameServerAddress), font=('Purisa', fontSize))
        self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(1/2)+fontSize*2, text='press <q> to return back to menu'.format(address=self.gameServerAddress), font=('Purisa', fontSize))

    def gameSSpectatingStateOnEnd(self):
        pass

    # -------------------- state: game.playing -------------------- #
    #
    # events: keyPressed
    #
    def gameSPlayingStateOnKeyPressed(self, event):
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
        elif key == 'q':
            self.gameSStateManager.setState('game.spectating')

        if vel != None:
            message = {
                'vel': {
                    'x': vel[0],
                    'y': vel[1],
                },
            }

            changeXYMessage = self.gameSGameClient.communicate('changeVel', message)

    def gameSPlayingStateOnStart(self):
        startPlayingMessage = self.gameSGameClient.communicate('startPlaying', {})

        error = {}# addPlayerMessage['error']

        if len(error) != 0:
            if error['title'] == 'GameFull':
                errorMessage = 'game server is full try again later'
            else:
                errorMessage = 'Unknown error occured'

            self.error = {
                'message': errorMessage
            }

            self.gameSStateManager.endState()
            self.stateManager.setState('main')

    def gameSPlayingStateOnLoop(self):
        self.canvas.delete('all')

        playersDict = self.gameSGameClient.communicate('loop', {})['players']
        players = []

        for playerDict in playersDict:
            if playerDict['playing']:
                players.append(Player.fromDict(playerDict))

        for player in players:
            player.draw(self)

        self.gameSMap.maze.draw(self)

    def gameSPlayingStateOnEnd(self):
        startPlayingMessage = self.gameSGameClient.communicate('endPlaying', {})

    # -------------------- state: main -------------------- #
    #
    # events: keyPressed
    #
    def mainStateOnKeyPressed(self, event):
        key = event.keysym

        if key == 'space':
            self.stateManager.setState('game')
        elif key == 'q':
            self.end()

    def mainStateOnStart(self):
        pass

    def mainStateOnLoop(self):
        self.canvas.delete('all')

        screenSizeX = self.screenSize[0]
        screenSizeY = self.screenSize[1]
        fontSize = self.fontSize(8)

        self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(5/8)-fontSize, text='server ip address: {address}'.format(address=self.gameServerAddress), font=('Purisa', self.fontSize(8)))
        self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(5/8)+fontSize, text='server port: {port}'.format(port=self.gameServerPort), font=('Purisa', self.fontSize(8)))
        self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(6/8)-fontSize, text='this game GUI was made using tkinter', font=('Purisa', self.fontSize(8)))
        self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(6/8)+fontSize, text='so please xpect some wierd crashes', font=('Purisa', self.fontSize(8)))
        self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(7/8)-fontSize, text='made by Tomas Sumsala', font=('Purisa', self.fontSize(8)))
        self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(7/8)+fontSize, text='github: qahSgiB/DartServerTest', font=('Purisa', self.fontSize(8)))

        if len(self.error) > 0:
            self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(1/2)-fontSize*2, text='press <space> to start game', font=('Purisa', self.fontSize(8)))
            self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(1/2)           , text='press <q> to exit', font=('Purisa', self.fontSize(8)))
            self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(1/2)+fontSize*2, text=self.error['message'], font=('Purisa', self.fontSize(8)))
        else:
            self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(1/2)-fontSize, text='press <space> to start game', font=('Purisa', self.fontSize(8)))
            self.canvas.create_text(screenSizeX*(1/2), screenSizeY*(1/2)+fontSize, text='press <q> to exit', font=('Purisa', self.fontSize(8)))

    def mainStateOnEnd(self):
        self.error = {}



snakeStyles = {
    'style1': PlayerRemoteX(Style(Style.styleSnakePlayer1Draw), Style(Style.styleSnakeRemote1Draw))
}
mazeStyles = {
    'style1': Style(Style.styleMaze1Draw)
}



def main():
    serverAddress = '192.168.1.3'
    serverPort = 4042

    game = Game([400, 400], serverAddress, serverPort)



if __name__ == '__main__':
    main()
