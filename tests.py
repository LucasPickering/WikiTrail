#!/usr/bin/env PYTHON3

import os
import sys
import wikitrail

TEST_ARTICLES = ['Rose', 'Pokemon', 'America', 'Kitchen', 'Barack_Obama']


def main():
    print("Running tests. . .")
    wikitrail.main(TEST_ARTICLES)
    print("Finished running tests")

if __name__ == '__main__':
    main()
