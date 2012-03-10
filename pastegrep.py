#!/usr/bin/env python
from time import sleep
from urllib import urlencode
from urllib2 import urlopen
from re import search, I, M
from os import mkdir
from os.path import isdir, exists
outdir = 'pastes'

def save_paste(identifier, data):
    fname = "{}/paste_{}.txt".format(outdir, identifier)
    with open(fname, 'w') as out:
        out.write(data)
    print "Saved {}".format(fname)

def pastegrep(expression, cb=save_paste, interval=20, endpoint='http://pastebin.com/ajax/realtime_data.php'):
    """Loops endlessly and grabs the index of recent pastes from pastebin.
    Whenever a new paste is discovered, it is fetched and evaluated against
    `expression`.  If `expression` is found inside the paste, the callback `cb`
    is called with the paste identifier and body data.  The `interval` is a
    time in seconds, and the endpoint is a pastebin.com URL with a listing
    recent pastes to scrape."""
    while True:
        fetch(expression, endpoint)
        sleep(interval)

seen = set()
def fetch(expression, url):
    if not isdir(outdir) and not exists(outdir):
        mkdir(outdir)

    feed = urlopen(url)
    for line in feed:
        if "created a new" in line:
            match = search(r'\[<a href="/(.*?)">.*?</a>\]', line)
            if match:
                identifier = match.groups()[0]
                if identifier not in seen:
                    handle_paste(identifier, expression)
                    seen.add(identifier)

def handle_paste(identifier, expression, save_func=save_paste):
    url = "http://pastebin.com/raw.php?i={}".format(identifier)
    try:
        data = urlopen(url).read()
        if search(expression, data, I|M):
            save_func(identifier, data)
    except Exception as e:
        print "Caught an exception: {}".format(e)
        print "URL was {}".format(url)

if __name__ == "__main__":
    from sys import argv
    if len(argv) <= 1: expression = 'password'
    else: expression = argv[1]

    print "Fetching all pastes that match the regular expression '{}'".format(expression)
    pastegrep(expression)
