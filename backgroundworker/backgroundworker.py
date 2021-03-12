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
def fetchNextPano(data):  # Receives dict with pwd and filename
    if isinstance(data, dict):
        if data.get('pwd', None) is None:
            print('Invalid dict, without pwd credentials')
            return

        if verifyServerOrigin(bytes(data['pwd'], 'utf-8')):
            panoid, lat, long, loc_name, countryname = getRandomPanorama(
                urban=data['params']['urban'],
                indoors=data['params']['indoors'],
                countryNumber=data['params']['countryNumber'])

            print(data['params'])
            print(panoid, lat, long, loc_name, countryname)
            download_pano(panoid, 'downloaded.png')

            # Downloaded move to static
            srcfile = Path(__file__).parent / 'downloaded.png'
            dstfile = (Path(__file__).parent.parent / 'web' / 'static'
                       / 'panos' / data['filename'])
            #
            copyfile(srcfile, dstfile)
            pwd = FCrypt.encrypt(bytes(BackgroundPass, 'utf-8'))
            pwd = pwd.decode('utf-8')
            sio.emit('fetchNextPano-done',
                     {'pwd': pwd, 'panoid': panoid, 'lat': lat, 'long': long,
                      'loc_name': loc_name, 'countryname': countryname,
                      'filename': data['filename']},
                     namespace='/background')
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
