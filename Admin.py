import sys
import string
import secrets
from flask import request, render_template, current_app


def generateToken(n):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(n))


def AdminSetup(app, socketio, PanoGame):
    AdminPass = generateToken(25)
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

    @ socketio.on('admin-startGame')
    def adminStartGame(json):
        if isinstance(json, dict):
            if json.get('pwd', None) != AdminPass:
                return

            PanoGame.startGame()

    @socketio.on('admin-endRound')
    def adminEndRound(json):
        if isinstance(json, dict):
            if json.get('pwd', None) != AdminPass:
                return

    @ socketio.on('admin-debug')
    def debugCommand(json):
        if isinstance(json, dict):
            if json.get('pwd', None) != AdminPass:
                return

            print('access to debug', file=sys.stderr)
