#!/usr/bin/env python

# usage: run_test.py [-h] [-v VERBOSITY] [-d]
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -v VERBOSITY, --verbosity VERBOSITY
#                         Verbosity level
#   -d, --deamon          run tests on changes

import os
import unittest
import argparse
import inotify.adapters
from inotify.constants import IN_ATTRIB, IN_CREATE, IN_CLOSE_WRITE, IN_DELETE, IN_MOVED_FROM, IN_MOVED_TO

excluded_path = [".git"]
excluded_file = [".pyc"]
valid_mask = reduce(lambda x,y: x|y, [IN_ATTRIB, IN_CREATE, IN_CLOSE_WRITE, IN_DELETE, IN_MOVED_FROM, IN_MOVED_TO])

def is_valid_path(path):
	return not any([ p in path for p in excluded_path])

def is_valid_filename(filename):
	return not any([ filename.endswith(f) for f in excluded_file ])

def seek_and_run(root_path=".", verbosity=1):
	test_runner = unittest.TextTestRunner(verbosity=verbosity)
	test_case = unittest.defaultTestLoader.discover(root_path)
	test_runner.run(test_case)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbosity', default=1, help='Verbosity level')
	parser.add_argument('-d', '--deamon', default=False, action="store_true", help='run tests on changes')
	args = parser.parse_args()

	root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
	seek_and_run(root_path=root_path, verbosity=args.verbosity)

	if args.deamon:
		i = inotify.adapters.InotifyTree(root_path, mask=valid_mask)
		for event in i.event_gen():
			if event is not None:
				(header, type_names, path, filename) = event
				if is_valid_path(path) and is_valid_filename(filename):
					seek_and_run(root_path=root_path, verbosity=args.verbosity)
