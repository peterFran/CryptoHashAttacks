#!/usr/bin/env python
# encoding: utf-8
"""
BruteForce.py

Created by Peter Meckiffe on 2013-02-15.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest
from hashlib import sha1
import time

class BruteForce:
	def __init__(self, hashtuple, salt):
		# Set alphabet, salt and tuple of hash values
		self.alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
		self.salt = salt
		self.hashtuple = hashtuple
		# Create a list of None values for collecting passwords
		self.passwordList = [None]*len(self.hashtuple)
		self.hashesMatched = 0
	
	def bruteAttack(self):
		# Start timer
		self.start = time.time()
		# Loop through all possible passwords, going to the deepest point of the hash first (aaaaaa)
		try:
			# Count through the alphabet adding each letter in the alphabet on, then exploring its children
			for a in self.alphabet:
				digest=sha1(self.salt + a).hexdigest()
				# If the password is found, handle in the foundItem method
				if digest in self.hashtuple:
					self.foundItem(a, digest)
				for b in self.alphabet:
					digest=sha1(self.salt + a+b).hexdigest()
					if digest in self.hashtuple:
						self.foundItem(a+b, digest)
					for c in self.alphabet:
						digest=sha1(self.salt + a+b+c).hexdigest()
						if digest in self.hashtuple:
							self.foundItem(a+b+c, digest)
						for d in self.alphabet:
							digest=sha1(self.salt + a+b+c+d).hexdigest()
							if digest in self.hashtuple:
								self.foundItem(a+b+c+d,digest)
							for e in self.alphabet:
								digest=sha1(self.salt + a+b+c+d+e).hexdigest()
								if digest in self.hashtuple:
									self.foundItem(a+b+c+d+e,digest)
								for f in self.alphabet:
									digest=sha1(self.salt + a+b+c+d+e+f).hexdigest()
									if digest in self.hashtuple:
										self.foundItem(a+b+c+d+e+f,digest)
		except:
			pass
		# Stop timer
		self.time_elapsed = time.time() - self.start
		# Give nice readout
		return self.finaliseOutput()
	
	# Format ouput when password found
	def foundItem(self, item, digest):
		elapsed_time = self.formatTime(time.time() - self.start)
		print "Found: %s matches %s Cracked in %s" % (item,digest,elapsed_time)
		self.passwordList[self.hashtuple.index(digest)] = "Password %s = %s\n\t Cracked in %s\n" % (item, digest, elapsed_time)
		
		# If all passwords found, exit program
		self.hashesMatched += 1
		if self.hashesMatched == len(self.hashtuple):
			raise Exception()
	
	# Method for formatting time output
	def formatTime(self, elapsed_time):
		if elapsed_time > 3600:
			hours = int(elapsed_time) / 3600
			mins = (int(elapsed_time) % 3600) / 60
			secs = elapsed_time % 60
			return "%d h, %d m, %f seconds, or %f seconds" % (hours, mins, secs, elapsed_time)
		elif elapsed_time > 60:
			mins = int(elapsed_time) / 60
			secs = elapsed_time % 60
			return "%d m, %f seconds, or %f seconds" % (mins, secs, elapsed_time)
		else:
			return "%f seconds" % (elapsed_time)
	
	# Format printout into output string
	def finaliseOutput(self):
		if None in self.passwordList:
			output = "%d passwords not matched, apologies...\n" % (len(self.hashtuple) - self.hashesMatched)
		else:
			output = "All hashes cracked. Take that!\n"
		output+="Time taken = %f seconds\n" % self.time_elapsed
		output = "List of passwords:\n"
		for x in self.passwordList:
			if x is None:
				output += "Hash not found at this index.\n"
			else:
				output += x
		return output
	
if __name__ == '__main__':
	hashes = ("c2543fff3bfa6f144c2f06a7de6cd10c0b650cae",
	"b47f363e2b430c0647f14deea3eced9b0ef300ce",
	"e74295bfc2ed0b52d40073e8ebad555100df1380",
	"0f7d0d088b6ea936fb25b477722d734706fe8b40",
	"77cfc481d3e76b543daf39e7f9bf86be2e664959",
	"5cc48a1da13ad8cef1f5fad70ead8362aabc68a1",
	"4bcc3a95bdd9a11b28883290b03086e82af90212",
	"7302ba343c5ef19004df7489794a0adaee68d285",
	"21e7133508c40bbdf2be8a7bdc35b7de0b618ae4",
	"6ef80072f39071d4118a6e7890e209d4dd07e504",
	"02285af8f969dc5c7b12be72fbce858997afe80a",
	"57864da96344366865dd7cade69467d811a7961b")
	saltedHashes = ("2cb3c01f1d6851ac471cc848cba786f9edf9a15b",
	"a20cdc214b652b8f9578f7d9b7a9ad0b13021aef",
	"76bcb777cd5eb130893203ffd058af2d4f46e495",
	"9208c87b4d81e7026f354e63e04f7a6e9ca8b535",
	"d5e694e1182362ee806e4b03eee9bb453a535482",
	"120282760b8322ad7caed09edc011fc8dafb2f0b"
	)
	a = BruteForce(saltedHashes,"uwe.ac.uk")
	print a.bruteAttack()
	a = BruteForce(hashes,"")
	print a.bruteAttack()
