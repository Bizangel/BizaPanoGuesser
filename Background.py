import secrets
import string
import sys
from cryptography.fernet import Fernet
from flask_socketio import emit
import subprocess
from pathlib import Path


def generateToken(n):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(n))


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

        # Start startRoundCountdown
        # enc = FCrypt.encrypt(bytes(BackgroundPass, 'utf-8'))
        # print('startingcountdown', file=sys.stderr)
        # emit('startRoundCountdown',
        #      {'pwd': enc.decode('utf-8'), 'seconds': 15},
        #      namespace='/background')

        # Start Fetchpano
        # enc = FCrypt.encrypt(bytes(BackgroundPass, 'utf-8'))
        # emit('fetchNextPano', enc.decode('utf-8'), namespace='/background')

    @socketio.on('fetchNextPano-done', namespace='/background')
    def panofetchdone(pwd):
        if isinstance(pwd, str):
            if (FCrypt.decrypt(bytes(pwd, 'utf-8')).decode('utf-8')
                    == BackgroundPass):
                print('Pano fetch was done Successfully!', file=sys.stderr)
        else:
            return

    @socketio.on('startRoundCountdown-done', namespace='/background')
    def countdowndone(pwd):
        if isinstance(pwd, str):
            if (FCrypt.decrypt(bytes(pwd, 'utf-8')).decode('utf-8')
                    == BackgroundPass):
                print('Countdown was done Successfully!', file=sys.stderr)
        else:
            return
