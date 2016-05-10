

"""
This is supposed to be the main script of our application.
"""
from Parser import Parser
import time

from config import enrollment_path
from config import verification_path
from signature import Signature

# timer
start_time = time.clock()


def print_timer(purpose_message=""):
    global start_time
    print("%s timer: %ss" % (purpose_message, int(time.clock()-start_time)))
    start_time = time.clock()

""" Reading Data """
parser = Parser(enrollment_path, verification_path)
enrollment_list = parser.parse_files_in_directory()
print enrollment_list[0]

print [[Signature("some data", "filename"), Signature("some data", "filename")],[Signature("some data", "filename"), Signature("some data", "filename")]]
