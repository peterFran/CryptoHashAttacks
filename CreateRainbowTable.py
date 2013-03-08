#!/usr/bin/env python
# encoding: utf-8
"""
CreateRainbowTable.py

Created by Peter Meckiffe on 2013-02-22.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
from hashlib import sha1


class CreateRainbowTable(object):
	def __init__(self):
		self.alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
		self.table={}
		self.reduce(sha1("hello").hexdigest(),78)
	def reduce(self, hashVal, cascadeLevel):
		hashVal = hashVal * cascadeLevel
		print hashVal
		length = (cascadeLevel % 6) + 1
		firstReduce = hashVal[0:length]
		out = ""
		for i in firstReduce:
			i = int(i) % len(self.alphabet)
			out+=self.alphabet[i]
		print out
	def createTable(self):
		pass
	def bruteAttack(self):
		try:
			for i in range(0,6):
				self.levelCascade("",i)
		except Exception as e:
			pass 
		return self.finaliseOutput()
	
	def levelCascade(self, previous, level):
		if level==0:
			for i in self.alphabet:
				digest = sha1(previous+i).hexdigest()
				if digest not in self.table:
					digest = sha1(digest[0:level]).hexdigest()
					if digest not in self.table:
						digest = sha1(digest[1:level+1]).hexdigest()
					self.passwordList[self.hashtuple.index(digest)] = "Password %s = %s\n" % (previous+i, digest)
					self.hashesMatched += 1
					if self.hashesMatched == self.tupleLength:
						raise Exception()
		else:
			for i in self.alphabet:
				self.levelCascade(previous+i, level-1)

if __name__ == '__main__':
	cr = CreateRainbowTable()