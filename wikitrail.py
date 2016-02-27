#!/usr/bin/python3

# Follows the wiki trail of a certain page to Philosophy. A wiki trail is the series of pages you
# get by starting at any page and continually following the first link in the main body of the
# article that's not in italics or parentheses. The theory is that this will always lead to
# Philosophy. Inspired by the alt-text of http://xkcd.com/903.

from urllib.request import urlopen
from urllib.error import HTTPError
import sys
import re

# Constants
destArticle = "philosophy"
wikiUrl = "http://en.wikipedia.org/wiki/"
bodyRegex = r'mw-body-content.*</div>'
pRegex = r'<p[^>]*>(.*?)</p>'
italicsRegex = r'<i>[^<]*</i>'
linkRegex = r'<a href="/wiki/(?!Help:)(.*?)"'

# Downloads and returns the html text for the wikipedia page by the given name
def getArticleHtml(name):
    try:
        return urlopen(wikiUrl + name).read().decode('cp1252', 'ignore')
    except HTTPError as err:
        print("Error loading page {} - code {}", name, err.code)

# Returns the name of the first article linked in the given html text, in all lower case
def getNextArticleName(page):
    page = ''.join(re.findall(pRegex, page, re.DOTALL)) # Get everything in <p> tags
    page = re.sub(italicsRegex, '', page) # Strip out everything in italics
    page = stripParens(page) # Strip out everything in parentheses
    page = re.findall(linkRegex, page, re.DOTALL)[0] # Get the first wiki link
    return page

def stripParens(s):
    inQuotes = False
    inParens = False
    result = ""
    for c in s:
        if c == '"':
            inQuotes = not inQuotes
        elif c == '(':
            inParens = True
        elif c == ')':
            inParens = False
        if inQuotes or not inParens:
            result += c
    return result

# If no article name was passed in
if(len(sys.argv) < 2):
    print("You must enter an article name to start with")
    exit()

article = sys.argv[1] # Get the article name
trail = [article] # Initialize a list to track the trail
while(article.lower() != destArticle.lower()): # While we haven't reached the destination...
    print("Working on " + article) # TODO: Remove this line
    article = getNextArticleName(getArticleHtml(article)) # Get the next article
    if article in trail: # IF the next article is already in the trail...
        # Print error and break
        print("Loop found! Call the internet police!")
        print("Found duplicate link to: " + article)
        break
    trail.append(article) # Add this article to the trail

# Print the trail
i = 1
for step in trail:
    print("{}. {}".format(i, step))
    i += 1
