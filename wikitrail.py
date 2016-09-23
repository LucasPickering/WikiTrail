#!/usr/bin/python3

# Follows the wiki trail of a certain page to Philosophy. A wiki trail is the series of pages you
# get by starting at any page and continually following the first link in the main body of the
# article that's not in italics or parentheses. The theory is that this will always lead to
# Philosophy. Inspired by the alt-text of http://xkcd.com/903.

from urllib.request import urlopen
from urllib.error import HTTPError
from operator import xor
import os
import sys
import re
import json
import traceback

# Constants
DEST_ARTICLE = "Philosophy"
wikiUrl = "http://en.wikipedia.org/wiki/"
SPAN_RGX = re.compile(r'<span[^>]*>.*?</span>', re.DOTALL)
TABLE_RGX = re.compile(r'<table[^>]*>.*?</table>', re.DOTALL)
P_RGX = re.compile(r'<p[^>]*>.*?</p>', re.DOTALL)
ITALICS_RGX = re.compile(r'<i>.*?</i>', re.DOTALL)
LINK_RGX = re.compile(r'<a href="/wiki/(?!Help:)(.*?)"', re.DOTALL)
JSON_FILE = 'trails.json'

# Downloads and returns the html text for the wikipedia page by the given name
def getArticleHtml(name):
    try:
        return urlopen(wikiUrl + name).read().decode('cp1252', 'ignore')
    except HTTPError as err:
        print("Error loading page {} - code {}", name, err.code)

# Returns the name of the first article linked in the given html text, in all lower case
def getNextArticleName(text):
    text = SPAN_RGX.sub('', text) # Strip out everything in a span tag
    text = TABLE_RGX.sub('', text) # Strip out all tables
    text = ''.join(P_RGX.findall(text)) # Get everything in <p> tags
    text = ITALICS_RGX.sub('', text) # Strip out everything in italics
    text = stripParens(text) # Strip out everything in parentheses, except parens inside quotes
    text = LINK_RGX.search(text).group(1) # Get the first wiki link
    return text

# Strip out everything inside parentheses, but not things in parentheses inside <a.../a>
def stripParens(s):
    inQuotes = False
    inParens = False
    result = ''

    for c in s: # For each character in the string...
        inQuotes = xor(inQuotes, c == '"') # Toggle whether or not we're in quotes
        inParens = (inParens or c == '(') and c != ')' # Track whether or not we're in parens
        if inQuotes or not inParens: # If we're in quotes or not in parens...
            result += c # Add this character to the result

    return result

def printTrail(trail):
    for i, step in enumerate(trail, 1):
        print("{}. {}".format(i, step))
    print('')

def traceArticle(article):
    trail = [article] # Initialize a list to track the trail
    while article != DEST_ARTICLE: # While we haven't reached the destination...
        articleText = getArticleHtml(article) # Get the text of the article body
        article = getNextArticleName(articleText) # Get the next article out of the article text
        trail.append(article) # Add this article to the trail

        if article in trail[:-1]: # If the most recent article is already in the trail...
            # Print error and break out (the trail will still get returned and pretty)
            print("Found duplicate link to: " + article)
            break
    return trail

def printerr(msg):
    print(msg, file=sys.stderr)

if __name__ == '__main__':
    # If no article name was passed in
    if len(sys.argv) < 2:
        printerr("Usage: {} <Starting article(s)>".format(sys.argv[0]))
        sys.exit(1)

    # Load previous results from JSON into a dict, or if they don't exist, make an empty dict
    if os.path.isfile(JSON_FILE):
        with open(JSON_FILE) as f:
            all_trails = json.load(f)
    else:
        all_trails = {}

    for article in sys.argv[1:]:
        print("Tracing {}. . .".format(article))
        sys.stdout.flush() # Flush to make sure it gets printed before it starts trailblazing
        try:
            trail = traceArticle(article) # Get the trail
            printTrail(trail) # Print the trail
            all_trails[article] = trail # Save the trail to the dict
        except Exception as e:
            printerr("Error from root article {}:".format(article))
            sys.stderr.flush()
            traceback.print_exc(file=sys.stderr)

    # Save all the data to the JSON file
    with open(JSON_FILE, 'w') as f:
        json.dump(all_trails, f, indent=4, sort_keys=True)

