import socketio
from RandomPanoDownloader.goodFetcher import getRandomPanorama
from RandomPanoDownloader.PanoDownloader import download_pano

from time import sleep
from pathlib import Path
from cryptography.fernet import Fernet
from shutil import copyfile
# Fetch tokens

file = open('secret.txt', 'r')
BackgroundPass = file.readline()[:-1]  # Remove \n
# Fernetkey = file.readline()
Fernetkey = bytes(file.readline(), 'utf-8')
file.close()
FCrypt = Fernet(Fernetkey)


sio = socketio.Client()


def verifyServerOrigin(pwd):
    return FCrypt.decrypt(pwd).decode('utf-8') == BackgroundPass


@ sio.event
def connect():
    print('Connection Established')


@ sio.event(namespace='/background')
def connectACK():
    print('acknowledged connection')


@ sio.event(namespace='/background')
def fetchNextPano(data):
    if isinstance(data, str):
        if verifyServerOrigin(bytes(data, 'utf-8')):
            panoid, lat, long, loc_name, countryname = getRandomPanorama(
                urban=True, indoors=False, countryNumber=None)

            print(panoid, lat, long, loc_name, countryname)
            download_pano(panoid, 'downloaded.png')
            pwd = FCrypt.encrypt(bytes(BackgroundPass, 'utf-8'))
            pwd = pwd.decode('utf-8')
            sio.emit('fetchNextPano-done', pwd, namespace='/background')
        else:
            print('unverified origin', data)
    else:
        print('invalid non-bytes received for panofetch pass')


@ sio.event(namespace='/background')
def startRoundCountdown(data):
    if isinstance(data, dict):
        if data.get('pwd', None) is None:
            print('Invalid dict, without pwd credentials')
            return

        if verifyServerOrigin(bytes(data['pwd'], 'utf-8')):
            # Do countdown
            sleep(data['seconds'])

            # reply back when done
            pwd = FCrypt.encrypt(bytes(BackgroundPass, 'utf-8'))
            pwd = pwd.decode('utf-8')
            sio.emit('startRoundCountdown-done', pwd, namespace='/background')
        else:
            print('unverified origin', data)
    else:
        print('invalid non-dict received for startRoundCountdown pass')


@ sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:6789', namespaces=['/background'])


sio.wait()
