import sys
import string
import secrets
from flask import request, render_template, current_app
from flask_socketio import emit, send


def generateToken(n):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(n))


def AdminSetup(app, socketio, PanoGame):
    # AdminPass = generateToken(25)
    AdminPass = '123'
    print('AdminPass=' + AdminPass, file=sys.stderr)

    @ app.route("/admin", methods=["GET", "POST"])
    def adminIntro():
        if request.method == 'POST':
            req = request.form

            auth = False
            if AdminPass == req.get('pwd', None):
                auth = True
            return render_template('adminPanel.html',
                                   authorized=auth, token=AdminPass)
        return app.send_static_file('admin.html')

    @socketio.on('connect', namespace='/admin')
    def adminConnect():
        print('admin connected', file=sys.stderr)

    @ socketio.on('admin-startGame', namespace="/admin")
    def adminStartGame(json):
        if isinstance(json, dict):
            if json.get('pwd', None) != AdminPass:
                return

            # Get everyone into the game

            print('Game Starting', file=sys.stderr)
            PanoGame.startGame(int(json['totalrounds']),
                               int(json['round_duration']))

            if not PanoGame.nextRound():  # If it's ready start, else get pano
                if not PanoGame.panoInqueue:  # If not in que, do it
                    send('Panorama is not ready!')
                    PanoGame.enqueuePano()
                # Make sure what you need for round starting
                PanoGame.startOnFetch = True
                print('Flag set', file=sys.stderr)

    @ socketio.on('admin-setPanoParams', namespace="/admin")
    def adminSetPanoParams(json):
        if isinstance(json, dict):
            if json.get('pwd', None) != AdminPass:
                return

            print(json, file=sys.stderr)
            PanoGame.setPanoParameters(
                urban=json['urban'], indoors=json['indoors'],
                countryNumber=json['countryNumber']
            )

    @socketio.on('admin-nextRound', namespace="/admin")
    def adminEndRound(json):
        if isinstance(json, dict):
            if json.get('pwd', None) != AdminPass:
                return

    @ socketio.on('admin-pano-enqueue', namespace='/admin')
    def EnqueuePano(json):
        if isinstance(json, dict):
            if json.get('pwd', None) != AdminPass:
                return

            PanoGame.enqueuePano()
            print('Pano was Enqueued', file=sys.stderr)

    @ socketio.on('admin-debug', namespace='/admin')
    def debugCommand(json):
        if isinstance(json, dict):
            if json.get('pwd', None) != AdminPass:
                return

            print('access to debug', file=sys.stderr)
            PanoGame.endRound()
