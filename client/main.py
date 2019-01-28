import time
import tkinter
import random

from libs.Game.GameClient import GameClient
from libs.Game.Mainloop import Mainloop
from libs.Game.State import StateManager



# -------------------- Style --------------------
#
#
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

    def styleBoost1Draw(boost, game):
        canvas = game.canvas
        gameMap = game.gameSMap

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        x = boost.pos[0]*scaleX
        y = boost.pos[1]*scaleY
        xSize = scaleX
        ySize = scaleY

        color = '#00BBDD'

        canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)

    def styleBoost2Draw(boost, game):
        canvas = game.canvas
        gameMap = game.gameSMap

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        x = boost.pos[0]*scaleX
        y = boost.pos[1]*scaleY
        xSize = scaleX
        ySize = scaleY

        color = '#33CC00'

        canvas.create_polygon(x, y+ySize/2, x+xSize/2, y+ySize, x+xSize, y+ySize/2, x+xSize/2, y, fill=color, outline=color)

# -------------------- Snake --------------------
#
#
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

class SnakeEliminator():
    def __init__(self, type, playerName=None):
        self.type = type
        self.playerName = playerName

    def getMessage(self):
        if self.type == 'maze':
            return 'eliminated by wall'
        elif self.type == 'snake':
            return 'eliminated by {name}'.format(name=self.playerName)

    def fromDict(snakeEliminatorDict):
        type = snakeEliminatorDict['type']
        if type == 'maze':
            return SnakeEliminator(type)
        elif type == 'snake':
            return SnakeEliminator(type, snakeEliminatorDict['playerName'])

# -------------------- Player --------------------
#
#
class Player():
    def __init__(self, id, name, playing, snake):
        self.id = id
        self.name = name

        self.playing = playing
        self.snake = snake

    def draw(self, game):
        self.snake.draw(game)

    def fromDict(playerDict):
        isPlayer = playerDict['isPlayer']
        playing = playerDict['playing']

        return Player(playerDict['id'], playerDict['name'], playing, Snake.fromDict(playerDict['snake'], isPlayer) if playing else None)

class PlayerRemoteX():
    def __init__(self, ifPlayer, ifRemote):
        self.ifPlayer = ifPlayer
        self.ifRemote = ifRemote

    def get(self, isPlayer):
        return self.ifPlayer if isPlayer else self.ifRemote

# -------------------- Boost --------------------
#
#
class Boost():
    def __init__(self, pos, style):
        self.pos = pos.copy()
        self.style = style

    def draw(self, game):
        self.style.draw(self, game)

    def fromDict(boostDict):
        return Boost([boostDict['x'], boostDict['y']], boostStyles[boostDict['style']])

# -------------------- Map+Maze --------------------
#
#
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
    def __init__(self, screenSize, gameServerAddress, gameServerPort, playerName):
        self.gameServerAddress = gameServerAddress
        self.gameServerPort = gameServerPort
        self.gameClient = None

        self.playerName = playerName

        self.screenSize = screenSize.copy()

        self.root = tkinter.Tk()
        self.root.geometry('{width}x{height}'.format(width=self.screenSize[0], height=self.screenSize[1]))
        self.root.protocol('WM_DELETE_WINDOW', self.end)
        self.root.title('Snako pythonish client GUI')
        self.root.resizable(False, False)

        self.canvas = tkinter.Canvas(self.root, width=self.screenSize[0], height=self.screenSize[1], bg='#FFFFFF', highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind_all('<Key>', lambda event: self.stateManager.event('keyPressed', event))

        self.after = self.canvas.after
        self.afterCancel = self.canvas.after_cancel

        self.stateManager = StateManager(self.after, self.afterCancel, 50)
        self.stateManager.addState('main', self.mainStateOnStart, self.mainStateOnLoop, self.mainStateOnEnd, {'keyPressed': self.mainStateOnKeyPressed})
        self.error = {}
        self.stateManager.addState('game', self.gameStateOnStart, self.gameStateOnLoop, self.gameStateOnEnd, {'keyPressed': self.gameStateOnKeyPressed})
        self.stateManager.addState('settings', self.settingsStateOnStart, self.settingsStateOnLoop, self.settingsStateOnEnd, {'keyPressed': self.settingsStateOnKeyPressed})

        self.stateManager.setState('main')

        self.root.mainloop()

    def fontSize(self, fontSize):
        return int(fontSize*(min(self.screenSize[0], self.screenSize[1])/400))

    def end(self):
        self.stateManager.endState()
        self.root.destroy()

    def createTexts(self, x, y, texts, fontSize):
        fontSize = self.fontSize(fontSize)

        textPos = -fontSize*(len(texts)-1)
        for i in range(len(texts)):
            self.canvas.create_text(x, y+textPos, text=texts[i], font=('Purisa', fontSize))
            textPos += 2*fontSize

    # -------------------- state: game -------------------- #
    #
    # events: keyPressed
    #
    def gameStateOnKeyPressed(self, event):
        self.gameSStateManager.event('keyPressed', event)

    def gameStateOnStart(self):
        self.gameSGameClient = GameClient(self.gameServerAddress, self.gameServerPort, True)
        self.gameSGameClient.begin()

        self.gameSStateManager = StateManager(self.after, self.afterCancel, 50)
        self.gameSStateManager.addState('game.playing', self.gameSPlayingStateOnStart, self.gameSPlayingStateOnLoop, self.gameSPlayingStateOnEnd, {'keyPressed': self.gameSPlayingStateOnKeyPressed})
        self.gameSStateManager.addState('game.spectating', self.gameSSpectatingStateOnStart, self.gameSSpectatingStateOnLoop, self.gameSSpectatingStateOnEnd, {'keyPressed': self.gameSSpectatingStateOnKeyPressed})
        self.gameSStateManager.addState('game.dead', self.gameSDeadStateOnStart, self.gameSDeadStateOnLoop, self.gameSDeadStateOnEnd, {'keyPressed': self.gameSDeadStateOnKeyPressed})

        initInfoMessage = self.gameSGameClient.communicate('initInfo', {})
        self.gameSMap = GameMap.fromDict(initInfoMessage['gameMap'], self.screenSize)

        addPlayerMessage = self.gameSGameClient.communicate('addPlayer', {'name': self.playerName})
        self.gameSPlayerId = addPlayerMessage['player']['id']

        self.gameSEliminator = None

        self.gameSStateManager.setState('game.spectating')

    def gameStateOnLoop(self):
        pass

    def gameStateOnEnd(self):
        self.gameSStateManager.endState()
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
            self.stateManager.setState('main')

    def gameSSpectatingStateOnStart(self):
        pass

    def gameSSpectatingStateOnLoop(self):
        self.canvas.delete('all')

        spectateDict = self.gameSGameClient.communicate('spectate', {})

        playersDict = spectateDict['players']
        players = []

        for playerDict in playersDict:
            players.append(Player.fromDict(playerDict))

        for player in players:
            if player.playing:
                player.draw(self)

        boostsDict = spectateDict['boosts']
        boosts = []

        for boostDict in boostsDict:
            boosts.append(Boost.fromDict(boostDict))

        for boost in boosts:
            boost.draw(self)

        self.gameSMap.maze.draw(self)

        screenSizeX = self.screenSize[0]
        screenSizeY = self.screenSize[1]
        fontSize = self.fontSize(8)

        remotePlayers = []
        for player in players:
            if player.id != self.gameSPlayerId:
                remotePlayers.append(player)

        playersText = ['players']
        createPlayerText = lambda player: '{name} playing'.format(name=player.name) if player.playing else '{name} spectating'.format(name=player.name)

        if len(remotePlayers) > 4:
            for i in range(3):
                playersText.append(createPlayerText(remotePlayers[i]))
            playersText.append('and {otherPlayersCount} other'.format(otherPlayersCount=len(remotePlayers)-3))
        else:
            for player in remotePlayers:
                playersText.append(createPlayerText(player))

        self.createTexts(screenSizeX*(1/2), screenSizeY*(1/2), ['spectating', 'your name is {name}'.format(name=self.playerName)], 8)
        self.createTexts(screenSizeX*(1/2), screenSizeY*(2/3), ['press <space> to start playing', 'press <q> to return back to menu'], 8)
        self.createTexts(screenSizeX*(1/2), screenSizeY*(5/6), playersText, 8)

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

            self.stateManager.setState('main')
        else:
            self.gamePlayingSEliminationResetAfter = None
            self.gamePlayingSEliminationId = None

    def gameSPlayingStateOnLoop(self):
        loopInfoDict = self.gameSGameClient.communicate('loopInfo', {})

        if loopInfoDict['dead']:
            self.gameSEliminator = SnakeEliminator.fromDict(loopInfoDict['deadInfo'])

            self.gameSStateManager.setState('game.dead')
        else:
            self.canvas.delete('all')

            loopDict = self.gameSGameClient.communicate('loop', {})

            playersDict = loopDict['players']
            players = []

            for playerDict in playersDict:
                players.append(Player.fromDict(playerDict))

            for player in players:
                if player.playing:
                    player.draw(self)

            boostsDict = loopDict['boosts']
            boosts = []

            for boostDict in boostsDict:
                boosts.append(Boost.fromDict(boostDict))

            for boost in boosts:
                boost.draw(self)

            self.gameSMap.maze.draw(self)

            if loopInfoDict['elimination']:
                if self.gamePlayingSEliminationId != None:
                    self.gamePlayingSEliminationId = None
                    self.afterCancel(self.gamePlayingSEliminationResetAfter)
                    self.gamePlayingSEliminationResetAfter = None

                self.gamePlayingSEliminationId = loopInfoDict['eliminationInfo']['playerName']
                self.gamePlayingSEliminationResetAfter = self.after(1000, self.gamePlayingSEliminationReset)

            if self.gamePlayingSEliminationId != None:
                screenSizeX = self.screenSize[0]
                screenSizeY = self.screenSize[1]

                self.createTexts(screenSizeX*(1/2), screenSizeY*(1/2), ['elimination {id}'.format(id=self.gamePlayingSEliminationId)], 8)

    def gameSPlayingStateOnEnd(self):
        startPlayingMessage = self.gameSGameClient.communicate('endPlaying', {})

        if self.gamePlayingSEliminationId != None:
            self.gamePlayingSEliminationId = None
            self.afterCancel(self.gamePlayingSEliminationResetAfter)
            self.gamePlayingSEliminationResetAfter = None

    def gamePlayingSEliminationReset(self):
        self.gamePlayingSEliminationId = None
        self.gamePlayingSEliminationResetAfter = None

    # -------------------- state: game.dead -------------------- #
    #
    # events: keyPressed
    #
    def gameSDeadStateOnKeyPressed(self, event):
        key = event.keysym

        if key == 'space':
            self.gameSStateManager.setState('game.spectating')
        if key == 'q':
            self.stateManager.setState('main')

    def gameSDeadStateOnStart(self):
        pass

    def gameSDeadStateOnLoop(self):
        self.canvas.delete('all')

        spectateDict = self.gameSGameClient.communicate('spectate', {})

        playersDict = spectateDict['players']
        players = []

        for playerDict in playersDict:
            players.append(Player.fromDict(playerDict))

        for player in players:
            if player.playing:
                player.draw(self)

        boostsDict = spectateDict['boosts']
        boosts = []

        for boostDict in boostsDict:
            boosts.append(Boost.fromDict(boostDict))

        for boost in boosts:
            boost.draw(self)

        self.gameSMap.maze.draw(self)

        screenSizeX = self.screenSize[0]
        screenSizeY = self.screenSize[1]

        self.createTexts(screenSizeX*(1/2), screenSizeY*(1/2), [self.gameSEliminator.getMessage(), 'press <space> to start playing', 'press <q> to return back to menu'], 8)

    def gameSDeadStateOnEnd(self):
        self.gameSEliminator = None

    # -------------------- state: main -------------------- #
    #
    # events: keyPressed
    #
    def mainStateOnKeyPressed(self, event):
        key = event.keysym

        if key == 'space':
            self.stateManager.setState('game')
        elif key == 'a':
            self.stateManager.setState('settings')
        elif key == 'q':
            self.end()

    def mainStateOnStart(self):
        pass

    def mainStateOnLoop(self):
        self.canvas.delete('all')

        screenSizeX = self.screenSize[0]
        screenSizeY = self.screenSize[1]

        mainTexts = ['press <space> to enter game', 'press <a> to enter settings', 'press <q> to exit']
        if len(self.error) > 0:
            mainTexts.append(self.error['message'])

        self.createTexts(screenSizeX*(1/2), screenSizeY*(1/2), mainTexts, 8)
        self.createTexts(screenSizeX*(1/2), screenSizeY*(5/8), ['server ip address: {address}'.format(address=self.gameServerAddress), 'server port: {port}'.format(port=self.gameServerPort)], 8)
        self.createTexts(screenSizeX*(1/2), screenSizeY*(3/4), ['this game GUI was made using tkinter', 'so please expect some wierd crashes'], 8)
        self.createTexts(screenSizeX*(1/2), screenSizeY*(7/8), ['made by Tomas Sumsala', 'github: qahSgiB/DartServerTest'], 8)

    def mainStateOnEnd(self):
        self.error = {}

    # -------------------- state: settings -------------------- #
    #
    # events: keyPressed
    #
    def settingsStateOnKeyPressed(self, event):
        key = event.keysym

        if self.settingsSChangeSetting == 'name':
            if key in list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                self.settingsSNewPlayerName += key
            elif key == 'BackSpace':
                if len(self.settingsSNewPlayerName) > 0:
                    self.settingsSNewPlayerName = self.settingsSNewPlayerName[:-1]
            elif key == 'space':
                if len(self.settingsSNewPlayerName) > 0:
                    self.playerName = self.settingsSNewPlayerName
                self.settingsSNewPlayerName = ''
                self.settingsSChangeSetting = None
        else:
            if key == 'a':
                self.settingsSChangeSetting = 'name'
                self.settingsSNewPlayerName = ''
            elif key == 'q':
                self.stateManager.setState('main')

    def settingsStateOnStart(self):
        self.settingsSChangeSetting = None
        self.settingsSNewPlayerName = ''

    def settingsStateOnLoop(self):
        self.canvas.delete('all')

        screenSizeX = self.screenSize[0]
        screenSizeY = self.screenSize[1]

        if self.settingsSChangeSetting == 'name':
            nameSettingsTexts = ['your new name is {name}'.format(name=self.settingsSNewPlayerName), 'type your new name', 'press <space> when you are done']
        else:
            nameSettingsTexts = ['press <a> to change your name', 'your current name is {name}'.format(name=self.playerName)]
        self.createTexts(screenSizeX*(1/2), screenSizeY*(1/3), nameSettingsTexts, 8)
        self.createTexts(screenSizeX*(1/2), screenSizeY*(2/3), ['press <q> to exit'], 8)

    def settingsStateOnEnd(self):
        pass



snakeStyles = {
    'style1': PlayerRemoteX(Style(Style.styleSnakePlayer1Draw), Style(Style.styleSnakeRemote1Draw))
}
mazeStyles = {
    'style1': Style(Style.styleMaze1Draw)
}
boostStyles = {
    'style1': Style(Style.styleBoost1Draw),
    'style2': Style(Style.styleBoost2Draw)
}



def main():
    import os

    serverAddress = '192.168.1.6'
    serverPort = 4042

    playerName = os.getlogin()

    game = Game([400, 400], serverAddress, serverPort, playerName)



if __name__ == '__main__':
    main()
