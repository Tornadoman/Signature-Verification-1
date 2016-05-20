class Signature:
    def __init__(self, data, filename):
        self.data = data
        self.filename = filename
        self.features = []

    def get_user(self):
        return self.filename[0:2]

    def is_genuine(self):
        if self.filename[4] == 'g':
            return True
        else:
            return False

    def get_number(self):
        return self.filename[-3:]

    def __str__(self):
        return ("%s: < %s >") % (self.filename, str(self.data), str(self.features))

    def get_feature(self):
        return self.features

    def set_features(self, features):
        self.features = features
