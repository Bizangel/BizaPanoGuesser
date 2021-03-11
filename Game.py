
from random import choice


class Panorama:

    def __init__(self, panoid, lat, long, loc_name):
        self.panoid = panoid
        self.lat = lat
        self.long = long
        self.loc_name = loc_name

    def __str__(self):
        return 'Panorama ID: {0}\nAt: {1} , {2} - {3}'.format(
            self.panoid,
            self.lat, self.long, self.loc_name)


class Game:
    Colors = ['aqua', 'black', 'blue', 'brown', 'deep_blue', 'green',
              'orange', 'purple', 'red', 'yellow']

    def __init__(self):
        self.value = 0
        self.round = -1  # Hasn't started

        self.nextPanoReady = False  # Consume on each round

        # self.panorama = Panorama(panoid, lat, long, loc_name)
        self.connected = {}  # Dict that maps sid -> username
        self.colors = {}  # Dict that maps sid -> colors
        self.next_panorama = None
        self.scores = {}

    def setPanorama(panorama):
        pass

    def startGame(self, socketioapp, appcontext):
        pass

    def endRound(self):
        pass

    def addPlayer(self, sid, username):
        '''Adds a player to the game, with the given username'''
        if username not in self.connected.values():
            self.connected[sid] = username
            notchosen = [color for color in Game.Colors
                         if color not in self.colors.values()]
            if len(notchosen) == 0:
                self.colors[sid] = choice(Game.Colors)  # Repeat colors
            else:
                self.colors[sid] = choice(notchosen)
            return True
        return False

    def removePlayerByName(self, username):
        ''' Removes a player by Username, returns True if player
        was successfully removed, returns False otherwise'''
        for sid in self.connected:
            if self.connected[sid] == username:
                self.removePlayer(sid)
                return True
        return False

    def removePlayer(self, sid):
        ''' Removes a player by SessionID, returns True if player
        was successfully removed, returns False otherwise'''
        if sid in self.connected:
            self.connected.pop(sid)
            self.colors.pop(sid)
            return True
        return False

    def getConnected(self):
        '''  Returns a json-like (dict) that contains all connected users,
        with their colors mapped '''
        newdict = {}
        for sid in self.connected:
            newdict[self.connected[sid]] = self.colors[sid]

        return newdict
