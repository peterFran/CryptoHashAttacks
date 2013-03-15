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
from Crypto import Random

class CreateRainbowTable(object):
	def __init__(self, maxStringLen, numChains, chainLength):
		self.alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
		self.table={}
		
		self.maxStringLen = maxStringLen
		self.numChains = numChains
		self.chainLength = chainLength
		self.maxVal = 0
		self.boundaries = []
		for i in range(0, self.maxStringLen):
			self.maxVal += len(self.alphabet)**(i+1)
			self.boundaries.append(self.maxVal)
		val = sha1("hi").hexdigest()
		self.reduceHash(val, 1)
	
	def getV(self, hashVal):
		modLength = int(hashVal, 16) % self.maxVal
		for index, val in enumerate(self.boundaries):
			if modLength <= val:
				return index+1
	
	def reduceHash(self, hashVal, cascadeLevel):
		intValue = int(hashVal, 16)
		self.reduceInt(intValue, cascadeLevel)
	
	def reduceInt(self, intVal, cascadeLevel):
		intVal = (intVal+cascadeLevel)*cascadeLevel
		modLength = intVal % self.maxVal
		return self.getStringValue(modLength)
	
	def getStringValue(self, intValue):
		stringVal = ""
		for index, boundary in enumerate(self.boundaries):
			if intValue >= boundary:
				stringVal+=self.alphabet[(intValue%boundary)%len(self.alphabet)]
	
	def createTable(self):
		for chain in range(1,self.numChains):
			random_integer = random.randint(0, self.maxStringLength)
			random_string = self.reduceInteger()
			
		
	
	def solve(self, hashValue):
		newHash = hashValue
		result = None
		for step in range(0,self.num_steps):
			start = self.checkTable(newHash)
			if start is None:
				newHash = sha1(self.reduce(newHash))
			else:
				return self.getPlainText(start, hashValue)
	
	def getPlainText(self, start, hashValue):
		reduced = start
		newHash = sha1(reduced)
		while newHash != hashValue:
			reduced = self.reduce(newHash)
			newHash = sha1(reduced)
		return reduced
	
	def checkTable(self, hashValue):
		for row in self.table:
			if hashValue == row["end"]:
				return row["start"]
		return None
	
	
	
if __name__ == '__main__':
	cr = CreateRainbowTable(6)
	
	
	
	
	
	