#!/usr/bin/python3

import os
import sys

testArticles = ['Rose', 'Pokemon', 'America']

print("Running tests...")
for article in testArticles:
	print("\nTesting " + article)
	sys.stdout.flush()
	os.system('python wikitrail.py ' + article)
print("\nFinished running tests")
