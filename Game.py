from time import time as epoch_seconds
from time import sleep
from random import choice
import sys
from vincenty import vincenty as geodistance
from flask_socketio import emit, join_room, leave_room, socketio
from Scorer import scorequantifier


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

        self.playerGuesses = {}  # Dict that maps sid -> lat lng objects

        self.inGame = False
        self.roundStarted = False
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
            {'pwd': enc.decode('utf-8'), 'seconds': self.round_duration,
             'round': self.round},
            namespace='/background', broadcast=True)

        print('countdown started')

    def endRound(self):
        '''Ends the round, DOES NOT START NEXT ROUND '''

        self.roundStarted = False

        RevealPano = self.panoramas[self.round]
        # Make Scores
        distances = {}
        sol_lat, sol_lng = RevealPano.lat, RevealPano.long

        # self.loc_name = loc_name
        # self.country_name = country_name
        # self.linkedstring = linkedstring

        for sid in self.connected:
            playerguess = self.playerGuesses.get(sid, None)
            if playerguess is None:
                playerguess = {'lat': 41.56203190200195,
                               'lng': -38.87721477590272}
                self.playerGuesses[sid] = playerguess  # Set for player display

            playerlatlng = (playerguess['lat'], playerguess['lng'])
            distances[sid] = geodistance(
                (sol_lat, sol_lng), playerlatlng)

        increase_scores = scorequantifier(distances)
        for sid in increase_scores:
            # Raise each corresponding obtained
            self.scores[sid] += increase_scores[sid]

        self.socketioapp.emit('leaderboard-update',
                              self.getScores(), room='lobby',
                              broadcast=True)

        usersguesses = {self.connected[sid]: self.playerGuesses[sid]
                        for sid in self.connected}
        usersguesses['SOLUTION'] = {'lat': sol_lat, 'lng': sol_lng}
        roundscores = {self.connected[sid]: increase_scores[sid]
                       for sid in self.connected}

        revealinfo = {
            'users_guesses': usersguesses,
            'roundscores': roundscores
        }
        self.socketioapp.emit('map-reveal', revealinfo, room='lobby',
                              broadcast=True)

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
        self.lockGuess = {}  # Maps to username -> True/False
        for sid in self.connected:
            self.lockGuess[self.connected[sid]] = False
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

            self.roundStarted = True
            # Emit at startgame and end round
            if self.round == 1:  # Only on first round
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

    def guessLock(self, sid, latlng):
        '''Locks the user guess with the given sid '''
        if self.inGame and self.roundStarted:
            if sid in list(self.connected.keys()):
                # verify latlng proper format
                if isinstance(latlng, dict):
                    if (latlng.get('lat', None) is not None and
                            latlng.get('lng', None) is not None):
                        # Proper lat long, accept
                        self.lockGuess[self.connected[sid]] = True
                        self.playerGuesses[sid] = latlng
                        # Emit update to everyplayer
                        self.socketioapp.emit(
                            'guess-update',
                            {'user': self.connected[sid], 'status': True},
                            room='lobby', broadcast=True)

                        # verify if everyone has locked
                        for player in self.lockGuess:
                            # If a single one hasn't locked, return
                            if not self.lockGuess[player]:
                                return
                        # If it finishes, finish round
                        self.endRound()

                else:
                    return
            else:
                return  # you're not in the game
        else:
            return  # Game hasn't started

    def guessUnlock(self, sid):
        '''Unlocks the user guess with the given sid '''
        if self.inGame and self.roundStarted:
            if sid in list(self.connected.keys()):
                self.lockGuess[self.connected[sid]] = False
                # Emit update to everyplayer
                self.socketioapp.emit(
                    'guess-update',
                    {'user': self.connected[sid], 'status': False},
                    room='lobby', broadcast=True)
            else:
                return  # you're not in the game
        else:
            return  # Game hasn't started
