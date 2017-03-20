#!/usr/bin/env python3

import wikitrail

TEST_ARTICLES = ['Rose', 'Pokemon', 'America', 'Kitchen', 'Barack_Obama']


def run_tests():
    print("Running tests...")
    wikitrail.main(*TEST_ARTICLES)
    print("Finished running tests")


if __name__ == '__main__':
    run_tests()
