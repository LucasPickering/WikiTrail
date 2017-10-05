#!/usr/bin/env python3

# Follows the wiki trail of a certain page to Philosophy. A wiki trail is the series of pages you
# get by starting at any page and continually following the first link in the main body of the
# article that's not in italics or parentheses. The theory is that this will always lead to
# Philosophy. Inspired by the alt-text of http://xkcd.com/903.

import argparse
import json
import re
import requests
import sys
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


class Trail(list):

    def __init__(self, starting_article):
        self.append(starting_article)

    def __str__(self):
        max_len = max(len(a) for a in self)
        lines = ['{}. {} {}'.format(i, article.ljust(max_len + 3), get_url(article)) for i, article in enumerate(self, 1)]
        return '\n'.join(lines)


def get_url(article):
    return WIKIPEDIA_URL.format(article)


# Downloads and returns the html text for the wikipedia page by the given name
def download_article(name):
    url = get_url(name)
    response = requests.get(url)
    if response.ok:
        return response.text
    print("Code {} loading '{}'".format(response.text, url), file=sys.stderr)


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
            print("Found duplicate link to: " + article)
            break

        trail.append(article)  # Add this article to the trail

    return trail


def main(*start_articles, dest_article=DEFAULT_DEST):
    all_trails = {}

    for article in start_articles:
        print("Tracing {}...".format(article))
        try:
            trail = trace_article(article, dest_article)  # Get the trail
            print(trail)  # Print the trail
            all_trails[article] = trail  # Save the trail to the dict
        except Exception:
            print("Error from root article {}:\n{}".format(article, traceback.format_exc()),
                  file=sys.stderr)
        print('')

    # Save all the data to the JSON file
    try:
        with open(JSON_FILE) as f:
            loaded = json.load(f)
    except FileNotFoundError:
        loaded = {}
    loaded.update(all_trails)
    with open(JSON_FILE, 'w') as f:
        json.dump(loaded, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get the trail of a Wikipedia article")
    parser.add_argument('start', nargs='+', help="Article(s) to start from (1 trail per entry)")
    parser.add_argument('--dest', '-d', default=DEFAULT_DEST, help="Destination article")
    args = parser.parse_args()
    main(*args.start, dest_article=args.dest)
