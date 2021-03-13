import secrets
import string
import sys
import os
import shutil
from cryptography.fernet import Fernet
from flask_socketio import emit
import subprocess
from pathlib import Path


class Panorama:

    def __init__(self, lat, long, loc_name, country_name, linkedstring):
        self.lat = lat
        self.long = long
        self.loc_name = loc_name
        self.country_name = country_name
        self.linkedstring = linkedstring

    def __str__(self):
        return 'Panorama ID: {0}\nAt: {1} , {2} - {3}'.format(
            self.panoid,
            self.lat, self.long, self.loc_name)


def clearPanoFolder():
    folder = Path(__file__).parent / 'web' / 'static' / 'panos'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def generateToken(n):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(n))


'''
BACKGROUND MAIN
'''


def BackgroundSetup(app, socketio, PanoGame):
    BackgroundPass = generateToken(25)
    Fernetkey = Fernet.generate_key()
    FCrypt = Fernet(Fernetkey)
    # write to backgroundworker
    file = open('backgroundworker/secret.txt', 'w')
    file.write(BackgroundPass)
    file.write('\n')
    file.write(Fernetkey.decode())
    file.close()

    PanoGame.setPanoFetchCredentials(FCrypt, BackgroundPass)  # Set and store

    # Clear panos folder
    clearPanoFolder()

    workerpath = str((Path(__file__).parent / 'backgroundworker'
                      / 'backgroundworker.py').absolute())

    workerdir = str((Path(__file__).parent / 'backgroundworker').absolute())
    # Once written, do subprocess
    subprocess.Popen(['python', workerpath],
                     creationflags=subprocess.CREATE_NEW_CONSOLE,
                     cwd=workerdir)

    @socketio.on('connect', namespace='/background')
    def backgroundConnect():
        print('background worker connected', file=sys.stderr)
        emit('connectACK')
        # PanoGame.enqueuePano()  # We need params to get the panorama

    @socketio.on('fetchNextPano-done', namespace='/background')
    def panofetchdone(data):
        if isinstance(data, dict):
            if data.get('pwd', None) is None:
                print('Invalid dict, without pwd credentials')
                return

            if (FCrypt.decrypt(bytes(data['pwd'], 'utf-8')).decode('utf-8')
                    == BackgroundPass):
                print('Pano fetch was done Successfully!', file=sys.stderr)
                PanoGame.setNextPanorama(
                    Panorama(data['lat'], data['long'],
                             data['loc_name'], data['countryname'],
                             data['filename'])
                )
                PanoGame.panoInqueue = False  # Done fetching

                if PanoGame.startOnFetch:
                    print('starting on fetch!', file=sys.stderr)
                    PanoGame.startOnFetch = False
                    PanoGame.nextRound()

        else:
            return

    @socketio.on('startRoundCountdown-done', namespace='/background')
    def countdowndone(data):
        if isinstance(data, dict):
            if data.get('pwd', None) is None:
                print('Invalid dict, without pwd credentials')
                return

            if (FCrypt.decrypt(bytes(data['pwd'], 'utf-8')).decode('utf-8')
                    == BackgroundPass):
                print('Countdown was done Successfully!', file=sys.stderr)
        else:
            return
