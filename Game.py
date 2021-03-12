from time import time as epoch_seconds
from time import sleep
from random import choice
import sys
from flask_socketio import emit, join_room, leave_room, socketio


class Game:
    Colors = ['aqua', 'black', 'blue', 'brown', 'deep_blue', 'green',
              'orange', 'purple', 'red', 'yellow']

    def __init__(self, socketioappinstance):
        self.value = 0
        self.round = 0  # Hasn't started

        self.socketioapp = socketioappinstance

        self.panoInqueue = False
        # Represents is a pano is the process of being fetched
        self.panoramas = {}  # Dict that maps round_number -> panorama string

        self.connected = {}  # Dict that maps sid -> username
        self.colors = {}  # Dict that maps sid -> colors
        self.scores = {}  # Dict that maps sid -> score

        self.inGame = False
        self.setPanoParameters()  # Set default parameters

        # Waiting on pano fetching params
        self.startOnFetch = False

    def setPanoFetchCredentials(self, FCrypt, BackgroundPass):
        self.FCrypt = FCrypt
        self.BackgroundPass = BackgroundPass

    def setPanoParameters(self, urban=True, indoors=False, countryNumber=None):
        self.urban = urban
        self.indoors = indoors
        self.countryNumber = countryNumber

    def enqueuePano(self):
        ''' Enqueues a pano to be fetched '''
        print('Enqueueing Pano', file=sys.stderr)
        self.panoInqueue = True
        timestamp = str(round(epoch_seconds()))
        enc = self.FCrypt.encrypt(bytes(self.BackgroundPass, 'utf-8'))
        params = {'urban': self.urban, 'indoors': self.indoors,
                  'countryNumber': self.countryNumber}
        self.socketioapp.emit(
            'fetchNextPano', {'pwd': enc.decode('utf-8'),
                              'filename': 'pano' + timestamp + '.png',
                              'params': params},
            namespace='/background', broadcast=True)

    def startRoundCountdown(self):
        ''' Starts round countdown, so nextRound will automatically be called
        when it returns '''
        enc = self.FCrypt.encrypt(bytes(self.BackgroundPass, 'utf-8'))
        self.socketioapp.emit(
            'startRoundCountdown',
            {'pwd': enc.decode('utf-8'), 'seconds': self.round_duration},
            namespace='/background', broadcast=True)

    def InGame(self):
        return self.inGame

    def setNextPanorama(self, panorama):
        self.panoramas[self.round + 1] = panorama  # Set next panorama
        print(self.panoramas)

    def startGame(self, total_rounds, round_duration):
        ''' Starts the game which will prevent players from joining
        Receives total number of rounds, and round duration in seconds '''

        self.round = 0
        self.inGame = True
        self.total_rounds = total_rounds
        self.round_duration = round_duration

        # LOCK the colors (not lobby ones)
        self.socketioapp.emit('color-set', self.getConnected(), room='lobby',
                              broadcast=True)  # else /admin

        print('Game Started!', file=sys.stderr)

    def switchAcknowledged(self, msg):
        print('nice', file=sys.stderr)
        self.socketioapp.join_room('game')

    def nextRound(self):
        '''Moves the game onto the next round,
        IF THE NEXT PANORAMA IS READY!, returns true on success, else returns
        false'''
        if (self.panoramas.get(self.round + 1, None) is not None
                and self.inGame):
            print('next round start')
            self.round += 1
            self.socketioapp.emit('leaderboard-update',
                                  self.getScores(), room='lobby',
                                  broadcast=True)

            roundupdate = {
                'countdown': round(epoch_seconds()) + self.round_duration,
                'totalrounds': self.total_rounds,
                'panostring': self.panoramas[self.round].linkedstring,
                'round': self.round
            }
            self.socketioapp.emit('round-update', roundupdate,
                                  room='lobby', broadcast=True)
            return True
        else:
            return False

    def addPlayer(self, sid, username):
        '''Adds a player to the game, with the given username'''
        if username not in self.connected.values() and not self.inGame:
            self.connected[sid] = username
            self.scores[sid] = 0
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
            self.scores.pop(sid)
            return True
        return False

    def getScores(self):
        '''  Returns a json-like(dict) that contains all connected users,
        with their scores mapped '''
        newdict = {}
        for sid in self.connected:
            newdict[self.connected[sid]] = self.scores[sid]

        return newdict

    def getConnected(self):
        '''  Returns a json-like(dict) that contains all connected users,
        with their colors mapped '''
        newdict = {}
        for sid in self.connected:
            newdict[self.connected[sid]] = self.colors[sid]

        return newdict
