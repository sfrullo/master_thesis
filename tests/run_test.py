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
valid_mask = reduce(lambda x,y: x|y, [IN_ATTRIB, IN_CREATE, IN_CLOSE_WRITE, IN_DELETE, IN_MOVED_FROM, IN_MOVED_TO])

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbosity', default=1, help='Verbosity level')
	parser.add_argument('-d', '--deamon', default=False, action="store_true", help='run tests on changes')
	args = parser.parse_args()

	test_runner = unittest.TextTestRunner(verbosity=args.verbosity)

	path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
	test_case = unittest.defaultTestLoader.discover(path)
	test_runner.run(test_case)

	if args.deamon:
		i = inotify.adapters.InotifyTree(path, mask=valid_mask)
		for event in i.event_gen():
			if event is not None:
				(header, type_names, path, filename) = event
				if not any([ p in path for p in excluded_path]):
					test_runner.run(test_case)

