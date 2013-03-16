#!/usr/bin/env python
# encoding: utf-8
"""
createTable.py

Created by Peter Meckiffe on 2013-03-16.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import getopt
from TableFactory import TableFactory


help_message = '''
The help message goes here.
'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
		except getopt.error, msg:
			raise Usage(msg)
	
		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-o", "--output"):
				output = value
		
		factory = TableFactory()
		table = factory.generateNewTable(int(argv[1]),int(argv[2]),int(argv[3]))
		table.writeOut("table.txt")
		
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
	sys.exit(main())
