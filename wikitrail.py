#!/usr/bin/env PYTHON3

# Follows the wiki trail of a certain page to Philosophy. A wiki trail is the series of pages you
# get by starting at any page and continually following the first link in the main body of the
# article that's not in italics or parentheses. The theory is that this will always lead to
# Philosophy. Inspired by the alt-text of http://xkcd.com/903.

import argparse
import json
import logging
import os
import re
import requests
import traceback

# Constants
DEFAULT_DEST = 'Philosophy'
WIKIPEDIA_URL = 'http://en.wikipedia.org/wiki/{}'
SPAN_RGX = re.compile(r'<span[^>]*>.*?</span>', re.DOTALL)
TABLE_RGX = re.compile(r'<table[^>]*>.*?</table>', re.DOTALL)
P_RGX = re.compile(r'<p[^>]*>.*?</p>', re.DOTALL)
ITALICS_RGX = re.compile(r'<i>.*?</i>', re.DOTALL)
LINK_RGX = re.compile(r'<a href="/wiki/(?!Help:)(.*?)"', re.DOTALL)
JSON_FILE = 'trails.json'

logging.basicConfig(format='{asctime} - {levelname} - {message}', datefmt='%Y-%m-%d %H:%M:%S',
                    style='{')


class Trail(list):

    def __init__(self, starting_article):
        self.append(starting_article)

    def __str__(self):
        return '\n'.join(['{}. {}'.format(i, article) for i, article in enumerate(self, 1)])


# Downloads and returns the html text for the wikipedia page by the given name
def download_article(name):
    url = WIKIPEDIA_URL.format(name)
    response = requests.get(url)
    if response.ok:
        return response.text
    logging.error("Code {} loading '{}'".format(response.text, url))


def extract_next_article(text):
    """
    Extracts the name of the first article linked in the given HTML that fits our criteria, and
    returns it.
    """
    text = SPAN_RGX.sub('', text)  # Strip out everything in a span tag
    text = TABLE_RGX.sub('', text)  # Strip out all tables
    text = ''.join(P_RGX.findall(text))  # Get everything in <p> tags
    text = ITALICS_RGX.sub('', text)  # Strip out everything in italics
    text = strip_parens(text)  # Strip out everything in parentheses, except parens inside quotes
    text = LINK_RGX.search(text).group(1)  # Get the first wiki link
    return text


# Strip out everything inside parentheses, but not things in parentheses inside quotes
def strip_parens(s):
    in_quotes = False
    in_parens = False
    result = ''

    for c in s:  # For each character in the string...
        in_quotes ^= c == '"'  # Toggle in_quotes if the character is a quote
        in_parens = (in_parens or c == '(') and c != ')'  # Track whether or not we're in parens
        if in_quotes or not in_parens:  # If we're in quotes or not in parens...
            result += c  # Add this character to the result

    return result


def trace_article(article, dest):
    trail = Trail(article)  # Initialize a Trail on the starting article
    while article != dest:  # While we haven't reached the destination...
        text = download_article(article)  # Get the text of the article body
        article = extract_next_article(text)  # Get the next article out of the article text

        if article in trail:  # If the most recent article is already in the trail...
            # Print error and break out (the trail will still get returned and pretty printed)
            logging.warning("Found duplicate link to: " + article)
            break

        trail.append(article)  # Add this article to the trail

    return trail


def main(*start_articles, dest_article=DEFAULT_DEST):
    # Load previous results from JSON into a dict, or if they don't exist, make an empty dict
    if os.path.isfile(JSON_FILE):
        with open(JSON_FILE) as f:
            all_trails = json.load(f)
    else:
        all_trails = {}

    for article in start_articles:
        logging.info("Tracing {}. . .".format(article))
        try:
            trail = trace_article(article, dest_article)  # Get the trail
            logging.info(trail)  # Print the trail
            all_trails[article] = trail  # Save the trail to the dict
        except Exception:
            logging.error("Error from root article {}:\n{}".format(article, traceback.format_exc()))

    # Save all the data to the JSON file
    with open(JSON_FILE, 'w') as f:
        json.dump(all_trails, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get the trail of a Wikipedia article")
    parser.add_argument('start', nargs='+', help="Article(s) to start from (1 trail per entry)")
    parser.add_argument('--dest', '-d', default=DEFAULT_DEST, help="Destination article")
    args = parser.parse_args()
    main(*args.start, args.dest)
