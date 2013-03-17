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
import random
import json
import time


class RainbowTable(object):
	def __init__(self, key_length, chain_length):
		self.alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
		self.table=[]
		self.key_length = key_length
		self.chain_length = chain_length
		self.maximum_value = 0
		self.boundaries = []
		for i in range(0, self.key_length):
			minumum_value = self.maximum_value
			self.maximum_value += len(self.alphabet)**(i+1)
			self.boundaries.append({"keyspace":len(self.alphabet)**(i+1), "max":self.maximum_value, "min":minumum_value})
		
	
	def reduceHash(self, hashVal, cascade_level):
		integer_value = int(hashVal, 16)
		return self.reduceInt(integer_value, cascade_level)
	
	def reduceInt(self, integer_value, cascade_level):
		#last_3_digits = int(str(integer_value)[-3:])
		# print "a ", integer_value
		# 		print "b ", last_3_digits
		integer_value = (integer_value%self.maximum_value)+(integer_value%(cascade_level+1))+(cascade_level)
		modulus_length = integer_value % self.maximum_value 
		string_value = ""
		for index, keyspace in enumerate(self.boundaries):
			if modulus_length < keyspace["max"] and modulus_length >= keyspace["min"]:
				modulus_length = modulus_length % keyspace["keyspace"]
				string_value= ""
				for i in range(0,index+1):
					string_value+= self.alphabet[(modulus_length/(len(self.alphabet)**i))%len(self.alphabet)]
				if string_value == None:
					print keyspace["keyspace"]
					print modulus_length
				return string_value
	
	def createTable(self, number_chains):
		for chain in range(0,number_chains):
			random_integer = random.randint(0, self.maximum_value)
			start_string = self.reduceInt(random_integer, 0)
			
			while self.checkTableStart(start_string) is True:
				random_integer = random.randint(0, self.maximum_value)
				start_string = self.reduceInt(random_integer, 0)
				print start_string
			end_hash = self.calculateChainFromString(start_string, 0)
			# print "New Chain:"
			# print "Start: ", start_string
			# print "End: ", end_hash
			
			self.table.append({"start":start_string, "end":end_hash})
			
	
	def writeOut(self, filename):
		f = open(filename, 'w')
		output_table = {"args":{"key_length":self.key_length,"chain_length":self.chain_length},"table":self.table}
		f.write(json.dumps(output_table))
		
	
	def checkTableStart(self, start_string):
		for row in self.table:
			if row["start"] == start_string:
				return True
	
	def checkTableEnd(self, hash_value):
		for row in self.table:
			if int(row["end"],16)==int(hash_value,16):
				return row["start"]
	
	def calculateChainFromString(self, start, first_step):
		last_reduced = start
		for stage in range(first_step, self.chain_length):
			hash_value = sha1(last_reduced).hexdigest()
			# print "hash: ",hash_value
			# print "stage: ",stage
			# print "from: ",last_reduced, "\n"
			this_reduced = self.reduceHash(hash_value,stage)
			last_reduced = this_reduced
		return hash_value
	
	def calculateChainFromHash(self, hash_value, first_step):
		next_hash = hash_value
		this_reduced = None
		for stage in range(first_step, self.chain_length):
			hash_value = next_hash
			this_reduced = self.reduceHash(next_hash,stage)
			next_hash = sha1(this_reduced).hexdigest()
		return hash_value
		
	def solve(self, hash_value):
		result = None
		start_time = time.time()
		for step in range(0, self.chain_length):
			step = self.chain_length-(step+1)
			end_hash = self.calculateChainFromHash(hash_value, step)
			
			start = self.checkTableEnd(end_hash)
			if start is not None:
				plain_text = self.getPlainText(start, step, hash_value)
				if plain_text is not None:
					time_found =  time.time() - start_time
					print "Password: ", plain_text, " found in: ", time_found, " seconds \n\t for hash value: ", hash_value
					return plain_text 
	
	def getPlainText(self, start, stage, hash_value_in):
		this_reduced = start
		for stage in range(0, stage):
			hash_value = sha1(this_reduced).hexdigest()
			this_reduced = self.reduceHash(hash_value,stage)
			# print "stage: ",stage
			# 			print "from: ",this_reduced
			# 			print "hash: ", sha1(this_reduced).hexdigest(),"\n"
		if sha1(this_reduced).hexdigest()==hash_value_in:
			return this_reduced
		else:
			return None
	

if __name__ == '__main__':
	factory = TableFactory()
	table = factory.importTableFromFile("table.txt")
	print table.calculateChainFromHash("c22b5f9178342609428d6f51b2c5af4c0bde6a42", 199823)
	#cr.solve("12c89b4e83c51649d8d68837a7cab5217be0a508")
	
# from TableFactory import TableFactory
# tf = TableFactory()
# tab = tf.importTableFromFile("table.txt")
# tab.reduceHash("04bec847678223d8ea989e2780d5bb0d2f0e9739", 991)
# tab.reduceHash("5276d64bf1e11211969bb0bf1d5f60348a4f96ef", 991)
	
	
	