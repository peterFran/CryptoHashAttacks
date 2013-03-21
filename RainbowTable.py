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
	### KEYSPACE = Number of possible keys
	### KEYLENGTH = Number of characters in the password
	def __init__(self, key_length, chain_length):
		# Alphabet field
		self.alphabet = "abcdefghijklmnopqrstuvwxyz"
		# Array containing chains
		self.table=[]
		# init values
		self.key_length = key_length
		self.chain_length = chain_length
		self.maximum_value = 0
		# create boundary table
		# this divides up the keyspace between each potential keylength e.g. 1 - 6
		self.boundaries = []
		for i in range(0, self.key_length):
			minumum_value = self.maximum_value
			self.maximum_value += len(self.alphabet)**(i+1)
			self.boundaries.append({"keyspace":len(self.alphabet)**(i+1), "max":self.maximum_value, "min":minumum_value})
		
	# Decorator function to convert hash to int and pass to reduceInt function
	def reduceHash(self, hashVal, cascade_level):
		integer_value = int(hashVal, 16)
		return self.reduceInt(integer_value, cascade_level)
	
	# Reduces an integer into an integer in the keyspace, and returns the textual representation of this
	def reduceInt(self, integer_value, cascade_level):
		# Reduce value into keyspace, with cascade level as an offset
		modulus_length = (integer_value+(cascade_level**self.key_length))%self.maximum_value
		
		# Convert integer to text
		string_value = ""
		# Use enumerate to get index value and row value
		for index, keyspace in enumerate(self.boundaries):
			if modulus_length < keyspace["max"] and modulus_length >= keyspace["min"]:
				# Get value into even smaller range
				modulus_length = modulus_length - keyspace["min"]
				string_value= ""
				# for each character get its text value in the alphabet
				for i in range(0,index+1):
					string_value+= self.alphabet[(modulus_length/(len(self.alphabet)**i))%len(self.alphabet)]
				return string_value
	
	# Create the rainbow table
	def createTable(self, number_chains):
		# Create the chains (note no threads, CPython doesn't natively use multiple cores, so no point threading)
		for chain in range(0,number_chains):
			# Create seed in keyspace
			random_integer = random.randint(0, self.maximum_value)
			# Get string relating to seed
			start_string = self.reduceInt(random_integer, 0)
			# Calculate final hash
			end_hash = self.calculateChainFromString(start_string, 0)
			print "step: ", chain
			# If the chain start/end is already in the table, do it all again
			while self.checkTableStart(start_string) is True or self.checkTableEnd(end_hash) :
				random_integer = random.randint(0, self.maximum_value)
				start_string = self.reduceInt(random_integer, 0)
				end_hash = self.calculateChainFromString(start_string, 0)
				print start_string
			# Append chain to the end of the table
			self.table.append({"start":start_string, "end":end_hash})
			
	
	# Write the table out to a file using JSON
	def writeOut(self, filename):
		f = open(filename, 'w')
		output_table = {"args":{"key_length":self.key_length,"chain_length":self.chain_length},"table":self.table}
		f.write(json.dumps(output_table))
		
	
	# Check table for start string
	def checkTableStart(self, start_string):
		for row in self.table:
			if row["start"] == start_string:
				return True
	
	# Check table for final hash value
	def checkTableEnd(self, hash_value):
		for row in self.table:
			if int(row["end"],16)==int(hash_value,16):
				return row["start"]
	
	# Calculate the end of a chain from a starting string
	def calculateChainFromString(self, start, first_step):
		# Keep last reduced value
		last_reduced = start
		# For all the stages until the end of the chain
		for stage in range(first_step, self.chain_length):
			# Get hash value from last reduce value
			hash_value = sha1(last_reduced).hexdigest()
			# Get the next reduce value
			last_reduced = self.reduceHash(hash_value,stage)
		return hash_value
	
	# Calculate the end of a chain from a hash value
	def calculateChainFromHash(self, hash_value, first_step):
		# Keep the next hash value and the reduced value (so if only one step, we return original hash)
		next_hash = hash_value
		# For all the stages until the end of the chain
		for stage in range(first_step, self.chain_length):
			# hash = last hash
			hash_value = next_hash
			# get next reduced
			this_reduced = self.reduceHash(next_hash,stage)
			# get next hash
			next_hash = sha1(this_reduced).hexdigest()
		return hash_value
		
	# Solve a hash based on this hash table
	def solve(self, hash_value):
		# Log the start time
		start_time = time.time()
		# For each link in the chain
		for step in range(0, self.chain_length):
			# (going backwards)
			step = self.chain_length-(step+1)
			
			# Get the end hash if hash was this step
			end_hash = self.calculateChainFromHash(hash_value, step)
			
			# Check if the end hash is in the table, if yes, get its start.
			start = self.checkTableEnd(end_hash)
			if start is not None:
				# Find the plain text at the link index
				plain_text = self.getPlainText(start, step, hash_value)
				# If plaintext matched, print out timing, and return password
				if plain_text is not None:
					time_found =  time.time() - start_time
					print "Password: ", plain_text, " found in: ", time_found, " seconds \n\t for hash value: ", hash_value
					return plain_text 
	
	# Count through the chain from the start to the given index and see if hashes match
	def getPlainText(self, start, stage, hash_value_in):
		this_reduced = start
		for stage in range(0, stage):
			hash_value = sha1(this_reduced).hexdigest()
			this_reduced = self.reduceHash(hash_value,stage)
		if sha1(this_reduced).hexdigest()==hash_value_in:
			return this_reduced
		else:
			return None
	
