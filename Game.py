
class Game:
    def __init__(self):
        self.value = 0
        self.connected = []

    def plus(self):
        self.value += 1

    def minus(self):
        self.value -= 1

    def getValue(self):
        return self.value

    def addPlayer(self, sid):
        self.connected.append(sid)

    def removePlayer(self, sid):
        self.connected.remove(sid)

    def getConnected(self):
        return len(self.connected)
