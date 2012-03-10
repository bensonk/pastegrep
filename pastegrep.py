#!/usr/bin/env python
from time import sleep
from urllib import urlencode
from urllib2 import urlopen
from re import search, I, M
from os import mkdir
from os.path import isdir, exists
outdir = 'pastes'

seen = set()
def fetch(expression, url='http://pastebin.com/ajax/realtime_data.php'):
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

def save_paste(identifier, data):
    fname = "{}/paste_{}.txt".format(outdir, identifier)
    with open(fname, 'w') as out:
        out.write(data)
    print "Saved {}".format(fname)

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
    if len(argv) <= 1:
        expression = 'password'
    else:
        expression = argv[1]

    print "Fetching all pastes that match the regular expression '{}'".format(expression)
    while True:
        fetch(expression)
        sleep(20)
