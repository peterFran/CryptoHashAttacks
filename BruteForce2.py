def badBruteAttack(self):
	try:
		self.depthFirst("",i)
	except Exception as e:
		pass 
	return self.finaliseOutput()
def depthFirst(self):
	for a in self.alphabet:
		digest=sha1(self.salt + a).hexdigest()
		if digest in self.hastuple:
			print "Found: %s matches %s" % (a,digest)
			self.passwordList[self.hashtuple.index(digest)] = "Password %s = %s\n" % (a, digest)
			return a
		for b in self.alphabet:
			digest=sha1(self.salt + a+b).hexdigest()
			if digest in self.hastuple:
				print "Found: %s matches %s" % (a+b,digest)
				self.passwordList[self.hashtuple.index(digest)] = "Password %s = %s\n" % (a, digest)
				return a+b
			for c in self.alphabet:
				digest=sha1(self.salt + a+b+c).hexdigest()
				if digest in self.hastuple:
					print "Found: %s matches %s" % (a+b+c,digest)
					self.passwordList[self.hashtuple.index(digest)] = "Password %s = %s\n" % (a+b+c, digest)
					return a+b+c
				for d in self.alphabet:
					digest=sha1(self.salt + a+b+c+d).hexdigest()
					if digest in self.hastuple:
						print "Found: %s matches %s" % (a+b+c+d,digest)
						self.passwordList[self.hashtuple.index(digest)] = "Password %s = %s\n" % (a+b+c+d, digest)
						return a+b+c+d
					for e in self.alphabet:
						digest=sha1(self.salt + a+b+c+d+e).hexdigest()
						if digest in self.hastuple:
							print "Found: %s matches %s" % (a+b+c+d+e,digest)
							self.passwordList[self.hashtuple.index(digest)] = "Password %s = %s\n" % (a+b+c+d+e, digest)
							return a+b+c+d+e
						for f in self.alphabet:
							digest=sha1(self.salt + a+b+c+d+e+f).hexdigest()
							if digest in self.hastuple:
								print "Found: %s matches %s" % (a+b+c+d+e+f,digest)
								self.passwordList[self.hashtuple.index(digest)] = "Password %s = %s\n" % (a+b+c+d+e+f, digest)
								return a+b+c+d+e+f