import time
import tkinter
import random

from libs.Game.GameClient import GameClient
from libs.Game.Mainloop import Mainloop
from libs.Game.State import StateManager
from libs.Youtube import YoutubeChannel



# -------------------- Style --------------------
#
#
class Style():
    def __init__(self, details):
        self.details = details

    def draw(obj, game):
        pass

    def fromDict(styleDict, styleType):
        return styles[styleType][styleDict['name']](styleDict['details'])

class StyleSnakeDefaultPlayer(Style):
    def draw(self, snake, game):
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

class StyleSnakeDefaultRemote(Style):
    def draw(self, snake, game):
        canvas = game.canvas
        gameMap = game.gameSMap

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        def blockToNBlock(baseBlock, block):
            xDist = block[0]-baseBlock[0]
            yDist = block[1]-baseBlock[1]
            xDistN = xDist/abs(xDist) if xDist != 0 else 0
            yDistN = yDist/abs(yDist) if yDist != 0 else 0

            return [xDistN, yDistN]

        blocks = snake.blocks
        for blockIndex in range(len(blocks)):
            block = blocks[blockIndex]

            if block.isHead:
                x = block.pos[0]*scaleX
                y = block.pos[1]*scaleY
                xSize = scaleX
                ySize = scaleY

                color = '#FF0000'

                canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)

            else:
                nBlocks = {
                    (0, 1): True,
                    (0, -1): True,
                    (1, 0): True,
                    (-1, 0): True,
                }

                if blockIndex > 0:
                    nBlocks[tuple(blockToNBlock(block.pos, blocks[blockIndex-1].pos))] = False
                if blockIndex < len(blocks)-1:
                    nBlocks[tuple(blockToNBlock(block.pos, blocks[blockIndex+1].pos))] = False

                blockX = block.pos[0]
                blockY = block.pos[1]

                for nBlock in nBlocks.keys():
                    if nBlocks[nBlock]:
                        nBlockX = nBlock[0]
                        nBlockY = nBlock[1]

                        x0 = None
                        x1 = None
                        if nBlockX == 0:
                            x0 = blockX
                            x1 = blockX+1
                        else:
                            if nBlockX < 0:
                                x0 = blockX
                                x1 = blockX
                            elif nBlockX > 0:
                                x0 = blockX+1
                                x1 = blockX+1

                        y0 = None
                        y1 = None
                        if nBlockY == 0:
                            y0 = blockY
                            y1 = blockY+1
                        else:
                            if nBlockY < 0:
                                y0 = blockY
                                y1 = blockY
                            elif nBlockY > 0:
                                y0 = blockY+1
                                y1 = blockY+1

                        canvas.create_line(x0*scaleX, y0*scaleY, x1*scaleX, y1*scaleY, fill='#000000')

class StyleSnakePewdiepiePlayer(Style):
    def draw(self, snake, game):
        canvas = game.canvas
        gameMap = game.gameSMap

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        for block in snake.blocks:
            x = block.pos[0]*scaleX
            y = block.pos[1]*scaleY
            xSize = scaleX
            ySize = scaleY

            color = '#FF0000'

            canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)

class StyleSnakePewdiepieRemote(Style):
    def draw(self, snake, game):
        canvas = game.canvas
        gameMap = game.gameSMap

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        def blockToNBlock(baseBlock, block):
            xDist = block[0]-baseBlock[0]
            yDist = block[1]-baseBlock[1]
            xDistN = xDist/abs(xDist) if xDist != 0 else 0
            yDistN = yDist/abs(yDist) if yDist != 0 else 0

            return [xDistN, yDistN]

        blocks = snake.blocks
        for blockIndex in range(len(blocks)):
            block = blocks[blockIndex]

            if block.isHead:
                x = block.pos[0]*scaleX
                y = block.pos[1]*scaleY
                xSize = scaleX
                ySize = scaleY

                color = '#FF0000'

                canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)

            else:
                nBlocks = {
                    (0, 1): True,
                    (0, -1): True,
                    (1, 0): True,
                    (-1, 0): True,
                }

                if blockIndex > 0:
                    nBlocks[tuple(blockToNBlock(block.pos, blocks[blockIndex-1].pos))] = False
                if blockIndex < len(blocks)-1:
                    nBlocks[tuple(blockToNBlock(block.pos, blocks[blockIndex+1].pos))] = False

                blockX = block.pos[0]
                blockY = block.pos[1]

                for nBlock in nBlocks.keys():
                    if nBlocks[nBlock]:
                        nBlockX = nBlock[0]
                        nBlockY = nBlock[1]

                        x0 = None
                        x1 = None
                        if nBlockX == 0:
                            x0 = blockX
                            x1 = blockX+1
                        else:
                            if nBlockX < 0:
                                x0 = blockX
                                x1 = blockX
                            elif nBlockX > 0:
                                x0 = blockX+1
                                x1 = blockX+1

                        y0 = None
                        y1 = None
                        if nBlockY == 0:
                            y0 = blockY
                            y1 = blockY+1
                        else:
                            if nBlockY < 0:
                                y0 = blockY
                                y1 = blockY
                            elif nBlockY > 0:
                                y0 = blockY+1
                                y1 = blockY+1

                        canvas.create_line(x0*scaleX, y0*scaleY, x1*scaleX, y1*scaleY, fill='#FF0000')

class StyleSnakeRainbowPlayer(Style):
    def draw(self, snake, game):
        canvas = game.canvas
        gameMap = game.gameSMap

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        colors = ['#9400D3', '#4B0082', '#0000FF', '#00FF00', '#FFFF00', '#FF7F00', '#FF0000']
        colorPhase = self.details['phase']

        colorIndex = colorPhase
        for block in snake.blocks:
            x = block.pos[0]*scaleX
            y = block.pos[1]*scaleY
            xSize = scaleX
            ySize = scaleY

            color = colors[colorIndex]

            canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)

            colorIndex -= 1
            if colorIndex < 0:
                colorIndex = len(colors)-1

class StyleSnakeRainbowRemote(Style):
    def draw(self, snake, game):
        canvas = game.canvas
        gameMap = game.gameSMap

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        colors = ['#9400D3', '#4B0082', '#0000FF', '#00FF00', '#FFFF00', '#FF7F00', '#FF0000']
        colorPhase = self.details['phase']

        colorIndex = colorPhase
        for block in snake.blocks:
            x = (block.pos[0]+0.2)*scaleX
            y = (block.pos[1]+0.2)*scaleY
            xSize = scaleX*0.6
            ySize = scaleY*0.6

            color = colors[colorIndex]

            canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)

            colorIndex -= 1
            if colorIndex < 0:
                colorIndex = len(colors)-1

class StyleMazeDefault(Style):
    def draw(self, block, game):
        canvas = game.canvas
        gameMap = game.gameSMap

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        x = block.pos[0]*scaleX
        y = block.pos[1]*scaleY
        xSize = scaleX
        ySize = scaleY

        color = '#0000FF'

        canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)

class StyleBoostFood(Style):
    def draw(self, boost, game):
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

class StyleBoostLgbt(Style):
    def draw(self, boost, game):
        canvas = game.canvas
        gameMap = game.gameSMap

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        x = boost.pos[0]*scaleX
        y = boost.pos[1]*scaleY
        xSize = scaleX
        ySize = scaleY

        canvas.create_text(x+xSize*(1/2), y+ySize*(1/3), text='NOT', font=('Purisa', int(ySize/3)))
        canvas.create_text(x+xSize*(1/2), y+ySize*(2/3), text='GOOD', font=('Purisa', int(ySize/3)), angle=180)

class StyleBoostPewdiepie(Style):
    def draw(self, boost, game):
        canvas = game.canvas
        gameMap = game.gameSMap

        scaleX = gameMap.scale[0]
        scaleY = gameMap.scale[1]

        x = boost.pos[0]*scaleX
        y = boost.pos[1]*scaleY
        xSize = scaleX
        ySize = scaleY

        color = '#FF0000'

        canvas.create_rectangle(x, y, x+xSize, y+ySize, fill=color, outline=color)

styles = {
    'snakePlayer': {
        'default': StyleSnakeDefaultPlayer,
        'rainbow': StyleSnakeRainbowPlayer,
        'pewdiepie': StyleSnakePewdiepiePlayer,
    },
    'snakeRemote': {
        'default': StyleSnakeDefaultRemote,
        'rainbow': StyleSnakeRainbowRemote,
        'pewdiepie': StyleSnakePewdiepieRemote,
    },
    'maze': {
        'default': StyleMazeDefault,
    },
    'boost': {
        'food': StyleBoostFood,
        'lgbt': StyleBoostLgbt,
        'pewdiepie': StyleBoostPewdiepie,
    },
}

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
    def __init__(self, blocks, style, score, activeBoostName):
        self.blocks = blocks
        self.style = style
        self.score = score
        self.activeBoostName = activeBoostName

    def draw(self, game):
        self.style.draw(self, game)

    def fromDict(snakeDict, isPlayer=False):
        blocks = [SnakeBlock.fromDict(blockDict) for blockDict in snakeDict['blocks']]

        styleDict = snakeDict['style']
        style = Style.fromDict(styleDict, 'snakePlayer' if isPlayer else 'snakeRemote')

        return Snake(blocks, style, snakeDict['score'], snakeDict['activeBoostName'])

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
        styleDict = boostDict['style']
        style = Style.fromDict(styleDict, 'boost')

        return Boost([boostDict['x'], boostDict['y']], style)

# -------------------- Map+Maze --------------------
#
#
class MazeBlock():
    def __init__(self, pos, style):
        self.pos = pos.copy()
        self.style = style

    def draw(self, game):
        self.style.draw(self, game)

    def fromDict(mazeBlockDict):
        styleDict = mazeBlockDict['style']
        style = Style.fromDict(styleDict, 'maze')

        return MazeBlock([mazeBlockDict['x'], mazeBlockDict['y']], style)

class Maze():
    def __init__(self, blocks):
        self.blocks = blocks.copy()

    def fromDict(mazeDict):
        blocks = []

        for blockDict in mazeDict['blocks']:
            blocks.append(MazeBlock.fromDict(blockDict))

        return Maze(blocks)

    def draw(self, game):
        for block in self.blocks:
            block.draw(game)

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

    def createTexts(self, x, y, texts, fontSize, font='Purisa'):
        fontSize = self.fontSize(fontSize)

        textPos = -fontSize*(len(texts)-1)
        for i in range(len(texts)):
            self.canvas.create_text(x, y+textPos, text=texts[i], font=(font, fontSize))
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
        self.gameSScore = None

        self.gameSErrorMessage = ''

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

        mainTexts = ['spectating', 'your name is {name}'.format(name=self.playerName)]

        if self.gameSErrorMessage != '':
            mainTexts.append(self.gameSErrorMessage)

        self.createTexts(screenSizeX*(1/2), screenSizeY*(1/2), mainTexts, 8)
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
        self.gameSErrorMessage = ''

        startPlayingMessage = self.gameSGameClient.communicate('startPlaying', {})

        error = startPlayingMessage['error']

        if len(error) != 0:
            if error['title'] == 'GameFull':
                errorMessage = 'game server is full try again later'
            else:
                errorMessage = 'unknown error occured'

            self.gameSErrorMessage = errorMessage

            self.gameSStateManager.setState('game.spectating')
        else:
            self.gamePlayingSEliminationResetAfter = None
            self.gamePlayingSEliminationId = None

            self.gameSScore = None

    def gameSPlayingStateOnLoop(self):
        loopInfoDict = self.gameSGameClient.communicate('loopInfo', {})

        if loopInfoDict['dead']:
            self.gameSEliminator = SnakeEliminator.fromDict(loopInfoDict['deadInfo'])

            self.gameSStateManager.setState('game.dead')
        else:
            loopDict = self.gameSGameClient.communicate('loop', {})

            playersDict = loopDict['players']
            players = []

            for playerDict in playersDict:
                players.append(Player.fromDict(playerDict))

            boostsDict = loopDict['boosts']
            boosts = []

            for boostDict in boostsDict:
                boosts.append(Boost.fromDict(boostDict))

            activeBoostName = ''
            for player in players:
                if self.gameSPlayerId == player.id:
                    self.gameSScore = player.snake.score

                    activeBoostName = player.snake.activeBoostName

            if loopInfoDict['elimination']:
                if self.gamePlayingSEliminationId != None:
                    self.gamePlayingSEliminationId = None
                    self.afterCancel(self.gamePlayingSEliminationResetAfter)
                    self.gamePlayingSEliminationResetAfter = None

                self.gamePlayingSEliminationId = loopInfoDict['eliminationInfo']['playerName']
                self.gamePlayingSEliminationResetAfter = self.after(1000, self.gamePlayingSEliminationReset)

            self.canvas.delete('all')

            screenSizeX = self.screenSize[0]
            screenSizeY = self.screenSize[1]

            if activeBoostName == 'pewdiepie':
                youtubeApiKey = 'AIzaSyCOcvg_f5GqfvO6sbjWLNO_TFNWJdURiJk'

                pewdiepieChannel = YoutubeChannel('pewdiepie', youtubeApiKey)
                tseriesChannel = YoutubeChannel('tseries', youtubeApiKey)

                subscriberGap = abs(pewdiepieChannel.getSubscribersCount()-tseriesChannel.getSubscribersCount())

                self.createTexts(screenSizeX*(1/2), screenSizeY*(1/2), ['SUBCRIBE TO', 'PEWDIEPIE'], 25, font='comic sans ms')
                self.createTexts(screenSizeX*(1/2), screenSizeY*(5/7), ['Current subscriber gap is 105235'], 8)

            for player in players:
                if player.playing:
                    player.draw(self)

            for boost in boosts:
                boost.draw(self)

            self.gameSMap.maze.draw(self)

            if self.gamePlayingSEliminationId != None:
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

        scoreMessage = 'your score is {score}'.format(score=self.gameSScore)

        self.createTexts(screenSizeX*(1/2), screenSizeY*(1/2), [self.gameSEliminator.getMessage(), scoreMessage, 'press <space> to start playing', 'press <q> to return back to menu'], 8)

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



def main():
    import os

    # serverAddress = '207.154.217.210'
    serverAddress = '192.168.1.4'
    serverPort = 4042

    playerName = os.getlogin()

    game = Game([400, 400], serverAddress, serverPort, playerName)



if __name__ == '__main__':
    main()
