import glob
class Parser(object):


    def __init__(self, directory):
        self.directory = directory

    def parseFilesInDirectory(self):
        paths = glob.glob(self.directory)
        parsedFile = map(self.parseFile,paths)
        return parsedFile

    def parseFile(self,path):
        lines = [line.rstrip('\n') for line in open(path)]
        measurements = map(self.parseFileToFeature, lines)
        return measurements

    def parseFileToFeature(self, line):

        desired_array = [float(numeric_string) for numeric_string in line.split()]
        return desired_array

    def main(self):
        lists = self.parseFilesInDirectory()
        for listFeature in lists:
            for feature in listFeature:
                print(feature)


if __name__ == "__main__": Parser("/home/sammer/signature_verification/Signature-Verification/enrollment/*.txt").main()