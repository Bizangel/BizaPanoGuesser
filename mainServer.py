import sys
from flask import Flask, request
from flask_socketio import SocketIO
from flask_socketio import emit
from Game import Game
# For emitting to specific client use it's sid on the room parameter of emit
app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
app.config['SECRET_KEY'] = 'secret!'

if len(sys.argv) == 2:
    ngroktunnel_public_url = sys.argv[1]
    print('Enabling Ngrok Tunneling On: ', ngroktunnel_public_url)
    socketio = SocketIO(app, cors_allowed_origins=ngroktunnel_public_url)
else:
    socketio = SocketIO(app)

PanoGame = Game()


@ app.route("/")
def hello():
    return app.send_static_file('sync.html')


def emitUpdateValue():
    emit('stateupdate', PanoGame.getValue(), broadcast=True)


def emitUpdateConnected():
    emit('connectedupdate', PanoGame.getConnected(), broadcast=True)


@socketio.on('minus')
def applyminus():
    PanoGame.minus()
    emitUpdateValue()


@socketio.on('plus')
def applyplus():
    PanoGame.plus()
    emitUpdateValue()


@socketio.on('connect')
def on_connect():
    PanoGame.addPlayer(request.sid)
    emitUpdateConnected()
    emit('stateupdate', PanoGame.getValue(), broadcast=False)
    # For whoever connected


@socketio.on('disconnect')
def on_disconnect():
    PanoGame.removePlayer(request.sid)
    emitUpdateConnected()

# chatroom test
# @ app.route("/")
# def hello():
#     return app.send_static_file('index.html')
#
#
# @ socketio.on('chat message')
# def on_chat_message(msg):
#     emit('chat message', msg, broadcast=True)
#
#
# @ socketio.on('connect')
# def on_connect():
#     print('A user connected', file=sys.stderr)
#
#
# @ socketio.on('disconnect')
# def on_disconnect():
#     print('A user connected', file=sys.stderr)


if __name__ == '__main__':
    SYNC_VALUE = 0
    socketio.run(app, debug=True, port=6789)
