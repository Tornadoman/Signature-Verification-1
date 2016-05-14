import glob
import os

from signature import Signature

def parse_validation_file(validation_path):
    validation_lines = [line.rstrip('\n') for line in open(validation_path)]
    parsed_validation = map(parse_validation_line, validation_lines)
    return parsed_validation

def parse_validation_line( validation_line):
    validation_vector = validation_line.split()
    filename_abbreviated = validation_vector[0]
    filename = validation_vector[0]
    genuine_or_fake = validation_vector[1] == 'g'
    return filename, genuine_or_fake

def get_filename_without_extension(path):
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

def parse_line_to_measurements(line):
    desired_array = [float(numeric_string) for numeric_string in line.split()]
    return desired_array


