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
srcpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for folder in os.listdir(srcpath):
	if os.path.isdir(os.path.join(srcpath, folder)):
		# path of the __tests__.py file
		tfile = os.path.join(srcpath, folder, "__tests__.py")
		if os.path.isfile(tfile):
			# run the unit tests
			begin_test(folder)		
			importlib.import_module(folder + ".__tests__").run_tests()
			end_test(folder)

show_summary()