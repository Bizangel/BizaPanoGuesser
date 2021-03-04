import sys
from pyngrok import ngrok
from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room
from flask_socketio import send, emit


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


@ app.route("/")
def hello():
    return app.send_static_file('index.html')


@ app.route("/js/socket.io.min.js")
def getsocketio():
    return app.send_static_file('js/socket.io.min.js')


@ socketio.on('chat message')
def on_chat_message(msg):
    emit('chat message', msg, broadcast=True)


@ socketio.on('connect')
def on_connect():
    print('A user connected', file=sys.stderr)


@ socketio.on('disconnect')
def on_disconnect():
    print('A user connected', file=sys.stderr)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=6789)
