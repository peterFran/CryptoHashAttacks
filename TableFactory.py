#!/usr/bin/env python
# encoding: utf-8
"""
TableFactory.py

Created by Peter Meckiffe on 2013-03-16.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
import json
from RainbowTable import RainbowTable


class TableFactory:
	def __init__(self):
		pass
	
	def generateNewTable(self, key_length, number_chains, chain_length):
		rainbow_table = RainbowTable(key_length, chain_length)
		rainbow_table.createTable(number_chains)
		return rainbow_table
		
	def importTableFromFile(self, filename):
		with open(filename, 'r') as f:
			stored_data = json.loads(f.read())
			key_length = stored_data['args']['key_length']
			chain_length = stored_data['args']['chain_length']
			table = stored_data['table']
			rainbow_table = RainbowTable(key_length, chain_length)
			rainbow_table.table = table
			return rainbow_table
		
	


class TableFactoryTests(unittest.TestCase):
	def setUp(self):
		pass

if __name__ == '__main__':
	factory = TableFactory()
	table = factory.importTableFromFile("table.txt")
	print table.calculateChainFromHash("c22b5f9178342609428d6f51b2c5af4c0bde6a42", 199823)
	print table.reduceHash("c22b5f9178342609428d6f51b2c5af4c0bde6a42", 199823)
	
	
	
	
	
	
	
	