import glob
import os
from config import enrollment_path
from config import verification_path
from signature import Signature
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
        return filenames

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
        filename = self.get_filename_without_extension(path)
        signature = Signature(measurements, filename)

        return signature

    def parse_line_to_measurements(self, line):
        desired_array = [float(numeric_string) for numeric_string in line.split()]
        return desired_array

if __name__ == "__main__":
    signatureList = Parser(enrollment_path, verification_path).parse_files_in_directory()
    for list in signatureList:
        print(list.get_number())