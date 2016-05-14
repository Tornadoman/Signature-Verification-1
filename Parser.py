import glob
import os

from signature import Signature

def get_filename_without_extension( path):
    base = os.path.basename(path)
    filename = os.path.splitext(base)[0]
    return filename

def parse_files_in_directory(directory):
    paths = glob.glob(directory)
    parsed_file = map(parse_file, paths)
    return parsed_file

def parse_file(path):
    lines = [line.rstrip('\n') for line in open(path)]
    measurements = map(parse_line_to_measurements, lines)
    filename = get_filename_without_extension(path)
    signature = Signature(measurements, filename)

    return signature

def parse_line_to_measurements(self, line):
    desired_array = [float(numeric_string) for numeric_string in line.split()]
    return desired_array


