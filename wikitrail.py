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
parenRegex = r'(?<!href=")\w*\([^)]*\)'
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
    #page = re.sub(parenRegex, '', page) # Strip out everything in parentheses
    page = stripParens(page) # Strip out everything in parentheses
    page = re.sub(italicsRegex, '', page) # Strip out everything in italics
    page = re.findall(linkRegex, page, re.DOTALL)[0] # Get the first wiki link
    return page

def stripParens(s):
    while '(' in s and ')' in s:
        openParen = s.index('(')
        closeParen = s[openParen:].index(')') + openParen
        rest = s[openParen:]
        s = s[:openParen] + rest[closeParen:]
    return s

# If no article name was passed in
if(len(sys.argv) < 2):
    print("You must enter an article name to start with")
    exit()

article = sys.argv[1]
trail = [article]
while(article.lower() != destArticle.lower()):
    print("Working on " + article)
    article = getNextArticleName(getArticleHtml(article))
    if article in trail:
        print("Loop found! Call the internet police!")
        print("Found duplicate link to: " + article)
        break
    trail.append(article)

i = 1
for step in trail:
    print("{}. {}".format(i, step))
    i += 1
