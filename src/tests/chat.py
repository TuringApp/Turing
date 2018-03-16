# -*- coding: utf-8 -*-

"""
CHAT : Clearly Horrible Automated Tester

Iterates all subfolders in src/ and runs unit tests.
"""

import os
from tests.framework import *
import importlib
import sys

# init the test environment
init_test()

# path of the main src/ folder
src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for folder in os.listdir(src_path):
    if os.path.isdir(os.path.join(src_path, folder)):
        # path of the __tests__.py file
        tests_file = os.path.join(src_path, folder, "__tests__.py")
        if os.path.isfile(tests_file):
            # run the unit tests
            begin_test(folder)
            importlib.import_module(folder + ".__tests__").run_tests()
            end_test(folder)

show_summary()
