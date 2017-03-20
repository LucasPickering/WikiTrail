#!/usr/bin/env PYTHON3

import os
import sys

testArticles = ['Rose', 'Pokemon', 'America', 'Kitchen']

print("Running tests. . .")
os.system('python wikitrail.py ' + ' '.join(testArticles))
print("Finished running tests")
