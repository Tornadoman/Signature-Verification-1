"""
This is supposed to be the main script of our application.
"""
import time

import Parser
import features
from DTW import DTW
from config import enrollment_path
from config import verification_gt_path
from config import verification_path

# timer
start_time = time.clock()


def print_timer(purpose_message=""):
    global start_time
    print("%s timer: %ss" % (purpose_message, int(time.clock() - start_time)))
    start_time = time.clock()


def sort_by_name(signature):
    return signature.filename


enrollment = sorted(features.calculate_features(Parser.parse_files_in_directory(enrollment_path)), key=sort_by_name)
verification = sorted(features.calculate_features(Parser.parse_files_in_directory(verification_path)), key=sort_by_name)
verification_gt = Parser.parse_validation_file(verification_gt_path)

print("enrollment names:")
for enr in enrollment[:5]:
    print(enr.filename)

print("verification names:")
for ver in verification[:5]:
    print(ver.filename)

print("verification-gt")
print(verification_gt)

for template in verification:
    dtw = DTW(template)

    results = [dtw.calculate_cost_and_matrix(enr) for enr in enrollment]
