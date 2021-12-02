from time import time as epoch_seconds
# from time import sleep
from random import choice
import sys
from vincenty import vincenty as geodistance
# from flask_socketio import emit, join_room, leave_room, socketio
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

    def enqueuePano(self, multires=True):
        ''' Enqueues a pano to be fetched '''
        print('Enqueueing Pano', file=sys.stderr)
        self.panoInqueue = True
        timestamp = str(round(epoch_seconds()))
        enc = self.FCrypt.encrypt(bytes(self.BackgroundPass, 'utf-8'))
        params = {'urban': self.urban, 'indoors': self.indoors,
                  'countryNumber': self.countryNumber}

        if multires:
            filename = 'pano' + timestamp
        else:
            filename = 'pano' + timestamp + '.png'
        self.socketioapp.emit(
            'fetchNextPano', {'pwd': enc.decode('utf-8'),
                              'filename': filename,
                              'params': params,
                              'multires': multires},
            namespace='/background', broadcast=True)

    def startRoundCountdown(self):
        ''' Starts round countdown, so endRound will automatically be called
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
            'roundscores': roundscores,
            'loc_name': RevealPano.loc_name,
            'country_name': RevealPano.country_name
        }
        self.socketioapp.emit('map-reveal', revealinfo, room='lobby',
                              broadcast=True)

        # Clear for next round
        self.lockGuess = {}  # Maps to username -> True/False
        for sid in self.connected:
            self.lockGuess[self.connected[sid]] = False

        self.playerGuesses = {}  # Clear all playerGuesses

    def InGame(self):
        return self.inGame

    def setNextPanorama(self, panorama):
        self.panoramas[self.round + 1] = panorama  # Set next panorama
        print(self.panoramas)

    def startGame(self, total_rounds, round_duration):
        ''' Starts the game which will prevent players from joining
        Receives total number of rounds, and round duration in seconds '''

        if len(self.connected) == 0:
            return False  # Can't start without players

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

        self.socketioapp.emit('game-starting-soon', room='lobby',
                              broadcast=True)
        print('Game Started!', file=sys.stderr)
        return True

    def switchAcknowledged(self, msg):
        print('nice', file=sys.stderr)
        self.socketioapp.join_room('game')

    def PanoIsReady(self):
        '''Returns true if next round pano is ready '''
        return self.panoramas.get(self.round + 1, None) is not None

    def endGame(self):
        # Replace then (in case there's less than three)
        allscores = self.getScores()
        gameRevealInfo = {
            'endleaderboard': allscores,
            'first': None,
            'second': None,
            'third': None,
        }

        max_score = max(allscores.values())
        if max_score == 0:
            max_score = 1  # Avoid stupid attacks
        for username, place in zip(
            sorted(allscores, key=allscores.get, reverse=True)[:3],
                ['first', 'second', 'third']):

            score = allscores[username]
            gameRevealInfo[place] = {
                'username': username,
                'scorepercent': round(score/max_score*100)}

        self.socketioapp.emit('game-reveal', gameRevealInfo,
                              room='lobby', broadcast=True)
        self.resetGameValues()  # Clean the game afterwards

    def resetGameValues(self):
        '''
        Game Finish Cleanup!
        '''
        self.inGame = False
        self.value = 0
        self.round = 0
        self.panoInqueue = False
        self.panoramas = {}
        self.connected = {}
        self.colors = {}
        self.scores = {}
        self.playerGuesses = {}
        self.lockGuess = {}  # Maps to username -> True/False
        self.inGame = False
        self.roundStarted = False
        self.setPanoParameters()
        self.startOnFetch = False

        print('Game reset cleaned!', file=sys.stderr)

    def nextRound(self):
        '''Moves the game onto the next round,
        IF THE NEXT PANORAMA IS READY!, returns true on success, else returns
        false'''

        if (not self.inGame):  # I'm not in game!
            return False

        # If it's last round, and it's done
        if (not self.roundStarted and self.round == self.total_rounds):
            # Finish the game
            self.endGame()
            return True

        # If pano is ready, if midgame, and NOT during another round:
        if (self.PanoIsReady() and not self.roundStarted):
            print('Moving to next round')
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

            # Start the countdown, give them extra seconds
            self.startRoundCountdown()

            self.enqueuePano()  # Start fetching the next panorama
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
            username = self.connected[sid]
            self.connected.pop(sid)
            self.colors.pop(sid)
            self.scores.pop(sid)

            if self.inGame:
                if self.playerGuesses.get(sid) is not None:
                    self.playerGuesses.pop(sid)

                self.lockGuess.pop(username)
                # Update that he left to everyone
                self.socketioapp.emit('leaderboard-update',
                                      self.getScores(), room='lobby',
                                      broadcast=True)

                if len(self.connected) == 0:  # If none connected
                    self.resetGameValues()
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

    def guessLockBackground(self, sid, latlng):
        '''Locks the user guess with the given sid '''
        if self.inGame and self.roundStarted:
            if sid in list(self.connected.keys()):
                # verify latlng proper format
                if isinstance(latlng, dict):
                    if (latlng.get('lat', None) is not None and
                            latlng.get('lng', None) is not None):
                        # Proper lat long, accept

                        # save it for the future
                        self.playerGuesses[sid] = latlng

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
