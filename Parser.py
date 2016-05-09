import glob
import os
from os.path import basename

class Parser(object):


    def __init__(self, directory,validation):
        self.directory = directory
        self.validationFile = validation

    def get_filename_without_extension(self, path):
        base = os.path.basename(path)
        filename = os.path.splitext(base)[0]
        return filename


    def get_filenames_without_extension(self):
        paths = glob.glob(self.directory)
        filenames = map(self.get_filename_without_extension, paths)
        print(*filenames, sep='\n')

    def parse_validation_file(self):
        validation_lines = [line.rstrip('\n') for line in open(self.validationFile)]
        parsed_validation = map(self.parse_validation_line, validation_lines)
        return parsed_validation



    def parse_validation_line(self,validation_line):
        validation_vector = validation_line.split()
        filename_abbreviated = validation_vector[0]
        filename = filename_abbreviated[:4] + 'g-' + filename_abbreviated[4:]
        genuine_or_fake = validation_vector[1]=='g'
        return filename, genuine_or_fake

    def parse_files_in_directory(self):
        paths = glob.glob(self.directory)
        parsed_file = map(self.parse_file, paths)
        return parsed_file

    def parse_file(self, path):
        lines = [line.rstrip('\n') for line in open(path)]
        measurements = map(self.parse_line_to_measurements, lines)
        return measurements

    def parse_line_to_measurements(self, line):
        desired_array = [float(numeric_string) for numeric_string in line.split()]
        return desired_array

    def main(self):
        lists = self.parse_files_in_directory()
        for listFeature in lists:
            for feature in listFeature:
                print(feature)



if __name__ == "__main__": Parser("/home/sammer/signature_verification/Signature-Verification/enrollment/*.txt","/home/sammer/signature_verification/Signature-Verification/verification-gt.txt").main()