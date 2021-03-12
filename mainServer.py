import sys
from flask import Flask, request
from flask_socketio import SocketIO
from flask_socketio import emit, send, join_room, leave_room
from Admin import AdminSetup
from Background import BackgroundSetup
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
    # socketio = SocketIO(app, logger=True, engineio_logger=True)


PanoGame = Game(socketio)

AdminSetup(app, socketio, PanoGame)
BackgroundSetup(app, socketio, PanoGame)


@ app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == 'POST':
        return app.send_static_file('lobby.html')
    return app.send_static_file('index.html')


@socketio.on('join-lobby')
def join_lobby(username):
    if isinstance(username, str):
        if len(username) < 5:
            send('Username is too short!')
            emit('invalid-join')
            return

        if username == 'SOLUTION' or username == 'ROUND':
            send('Invalid Name!')
            emit('invalid-join')

        if PanoGame.addPlayer(request.sid, username):
            join_room('lobby')
            send('Successfully Joined!')
            emit('valid-join')
            emit('lobby-update', PanoGame.getConnected(), room='lobby')
        else:
            if PanoGame.InGame():
                send('There\'s a game already in progress!')
            else:
                send('That username is already taken!')
                emit('invalid-join')


@socketio.on('leave-lobby')
def leave_lobby():
    leave_room('lobby')
    PanoGame.removePlayer(request.sid)  # Check if needs to be removed
    emit('lobby-update', PanoGame.getConnected(), room='lobby')
    send('You have left the lobby!')


@socketio.on('connect')
def test_connect():
    print('Client Connected', file=sys.stderr)


@socketio.on('disconnect')
def test_disconnect():
    # Player is automatically removed from lobby if he dces
    PanoGame.removePlayer(request.sid)  # Check if needs to be removed
    emit('lobby-update', PanoGame.getConnected(), room='lobby')  # Emit update


if __name__ == '__main__':
    SYNC_VALUE = 0
    socketio.run(app, debug=False, port=6789)
