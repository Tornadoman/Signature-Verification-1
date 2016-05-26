class Signature:
    def __init__(self, data, filename):
        self.data = data
        self.filename = filename
        self.cost = None


    def get_user(self):
        return self.filename[0:3]

    def is_genuine(self):
        if self.filename[4] == 'g':
            return True
        elif self.filename[4] == 'f':
            return False
        else:
            return None

    def get_number(self):
        return self.filename[-3:]

    def __str__(self):
        return ("%s: %s") % (self.filename, str(self.cost))

