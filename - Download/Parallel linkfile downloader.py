#!/usr/bin/python2

import os
from os.path import exists
from sys import argv, stdout, stderr
import random
import time

from pprint import pprint, pformat

import eventlet
from eventlet.green import urllib2

# default parameters
threads = 100
wait = 0.
randomNames = False
customdir = False


def randomUA():
    return 'Mozilla/{:.1f} (X{:.0f}; rv:{:.1f}) Firefox/{:.1f}'.format(
        random.random()*10.,
        random.random()*100.,
        random.random()*100.,
        random.random()*100.
        )


def randomHexString(l=80):
    return ''.join(random.choice('0123456789abcdefABCDEF') for _ in xrange(l))


def fetchFiles(name, url):
    if not exists(name):
        time.sleep(random.random() * wait)
        opener = urllib2.build_opener()
        opener.addheaders = [
                             ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                             ('Accept-Encoding', 'gzip, deflate'),
                             ('Connection', 'close'),
                             ('Proxy-Authorization', randomHexString()),
                             ('User-agent', randomUA())
                             ]
        r = opener.open(url)
        open(name, 'wb').write(r.read())
    else:
        stderr.write(name + ' already exists [' + url + ']\n')
    return name

if len(argv) < 2:
    print 'You have to specify file with links'
    exit()

for arg in argv:
    if arg.startswith('--help'):
        print '''\
Concurrent downloader
    uses greenlet.Pool

Usage: this-script-name [options] links-file

Options:
    --threads=int       Number of threads to download with (default={})
    --dir=str           Directory to download to (default=links-file)
    --randomnames       Give downloaded files random names (default={})
    --wait=float        Max time to wait between connections (default={})
'''.format(threads, randomNames, wait)
        exit()

    elif arg.startswith('--threads='):
        threads = int(arg.split('=')[-1])

    elif arg.startswith('--dir='):
        directory = arg.split('=')[-1]
        customdir = True

    elif arg.startswith('--randomnames'):
        randomNames = True

    elif arg.startswith('--wait='):
        wait = float(arg.split('=')[-1])

if not customdir:
    directory = argv[-1].strip() + '_downloaded_files/'

with open(argv[-1], 'r') as f:
    try:
        links = filter(bool, [x.strip() for x in f.readlines()])
    except IOError:
        stderr.write('Cannot open links file')
        exit()

    if directory and not directory.endswith('/'):
            directory += '/'

    if randomNames:
        names = [directory + randomHexString(l=30) +'.txt' for i in xrange(len(links))]
    else:
        names = list()
        for x in links:
            x = x.split()
            if len(x) == 2:
                names.append(x[1])
            else:
                names.append(directory + x[0].split('/')[-1])

print 'links count:', len(links)

try:
    os.mkdir(directory)
except OSError:
    print 'OSError -- mkdir -- folder may already exist'
    t = raw_input('Continue anyway? y/n')
    if t in ('Y', 'y'):
        exit()

pool = eventlet.GreenPool(threads)
l = len(names)

filesGot = 0
start = time.time()
for name in pool.imap(fetchFiles, names, links):
    filesGot += 1
    stdout.write('\r{} of {}'.format(filesGot, l))
    stdout.flush()

print
finish = time.time()
print 'Execution time:', finish - start

