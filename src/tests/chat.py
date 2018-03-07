# -*- coding: utf-8 -*-

"""
CHAT : Clearly Horrible Automated Tester

Iterates all subfolders in src/ and runs unit tests.
"""

import os
from .framework import *
import importlib.util
import sys

init_test()

srcpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for folder in os.listdir(srcpath):
	if os.path.isdir(os.path.join(srcpath, folder)):
		tfile = os.path.join(srcpath, folder, "__tests__.py")
		if os.path.isfile(tfile):
			begin_test(folder)
			spec = importlib.util.spec_from_file_location("tests", tfile)
			mod = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(mod)
			import mod
			#importlib.import_module(tfile)
			end_test(folder)