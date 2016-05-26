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
import csv

# timer
start_time = time.clock()
global output_list
output_list = []

""" Helper Functions"""


def print_timer(purpose_message=""):
    global start_time
    print("%s timer: %ss" % (purpose_message, int(time.clock() - start_time)))
    start_time = time.clock()


def sort_by_name(signature):
    return signature.filename


def apply_dtw(template):

    dtw = DTW(template)

    output = [template.get_user()]
    for enr in enrollment:
        if enr.get_user() == template.get_user():
            output.append(enr.filename)
            output.append(dtw.calculate_cost_and_matrix(enr))

    global output_list
    output_list.append(output)

    results = [dtw.calculate_cost_and_matrix(enr) for enr in enrollment if enr.get_user() == template.get_user()]
    template.cost = min(results)


""" Parsing """


enrollment = sorted(features.calculate_features(Parser.parse_files_in_directory(enrollment_path)), key=sort_by_name)
verification = sorted(features.calculate_features(Parser.parse_files_in_directory(verification_path)), key=sort_by_name)
# dev verification
# verification_gt = dict(Parser.parse_validation_file(verification_gt_path))
print_timer("parsing")


""" Applying DTW """


# adjust verification set size here
print("applying dtw. this might take a while")
for template in verification:
    apply_dtw(template)

print_timer("DTW")

# dev debug print
# print sorted([[verification[i].cost, verification_gt[verification[i].filename]] for i in range(len(verification))])

print(output_list)

with open("output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(output_list)
