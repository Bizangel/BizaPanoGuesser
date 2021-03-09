from RandomPanoDownloader.randomizer import getPanoFromCountryCode
from RandomPanoDownloader.PanoDownloader import download_pano
from pathlib import Path
from multiprocessing import Pool
from random import choice
from time import sleep
from flask_socketio import emit
import sys


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


def onPanoramaLoaded():
    pass


class Game:
    Colors = ['aqua', 'black', 'blue', 'brown', 'deep_blue', 'green',
              'orange', 'purple', 'red', 'yellow']

    def __init__(self):
        self.value = 0
        self.round = 1

        # Get initial base panorama
        # panoid, lat, long, loc_name = getPanoFromCountryCode(
        #     countryCode=None, outdoors=True)  # Truly Fully random
        panoid = '1SoWh9XHl1s6X7ACZXQvxw'
        lat, long = 61.39146458246076, 15.89755986088935
        loc_name = 'Gavleborg Country'

        self.panorama = Panorama(panoid, lat, long, loc_name)
        print(self.panorama)
        self.connected = {}  # Dict that maps sid -> username
        self.colors = {}  # Dict that maps sid -> colors
        self.next_panorama = None
        self.scores = {}

    def startGame(self, socketioapp, appcontext):
        pass

    def endRound(self):
        pass

    def getNextPanorama():
        filename = 'currentPano.png'
        filepath = str((Path(__file__).parent / 'web'
                        / 'static' / 'panos' / filename).absolute())
        pool = Pool(processes=1)
        pool.apply_async(async_postpone,
                         [10], callback=onPanoramaLoaded)

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
