
class Signature:
    def __init__(self, data, filename):
        self.data = data
        self.filename = filename

    def get_user(self):
        return self.filename[0:2]

    def isGenuine(self):
        if self.filename[4] == 'g':
            return True
        else:
            return False

    def getNumber(self):
        return self.filename[-3:]