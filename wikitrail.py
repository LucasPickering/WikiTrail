#!/usr/bin/python3
from urllib.request import urlopen
import re

url = "http://en.wikipedia.org/wiki/Potato"
bodyRegex = r'mw-body-content.*</div>'
pRegex = r'<p[^>]*>(.*?)</p>'
parenRegex = r'\([^)]*\)'
italicsRegex = r'<i>[^</i>]*</i>'
linkRegex = r'<a href="/wiki/(.*?)"'

page = urlopen(url).read().decode('utf-8') # Download the webpage
page = ''.join(re.findall(pRegex, page, re.DOTALL)) # Get everything in <p> tags
page = re.sub(parenRegex, '', page) # Strip out everything in parentheses
page = re.sub(italicsRegex, '', page) # Strip out everything in italics
page = re.findall(linkRegex, page, re.DOTALL)[0] # Get the first wiki link

print(page)
