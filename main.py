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

""" Helper Functions"""


def print_timer(purpose_message=""):
    global start_time
    print("%s timer: %ss" % (purpose_message, int(time.clock() - start_time)))
    start_time = time.clock()


def sort_by_name(signature):
    return signature.filename


def apply_dtw(template):

    dtw = DTW(template)

    results = [dtw.calculate_cost_and_matrix(enr) for enr in enrollment]
    min_cost = sorted(results)[0]
    print("results for template %s complete. Top result: %s" % (template.filename, max))
    template.cost = min_cost[0]


""" Parsing """


enrollment = sorted(features.calculate_features(Parser.parse_files_in_directory(enrollment_path)), key=sort_by_name)
verification = sorted(features.calculate_features(Parser.parse_files_in_directory(verification_path)), key=sort_by_name)
verification_gt = Parser.parse_validation_file(verification_gt_path)
print_timer("parsing")


""" Applying DTW """

# adjust verification set size here
for template in verification[:10]:
    apply_dtw(template)

print_timer("DTW")

for template in verification[:10]:
    print("%s, cost: %s" % (template.filename, template.cost))
