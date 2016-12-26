#!/usr/bin/python2

import os
import sys
import random
import time

from colorama import init

try:
    import eventlet
    from eventlet.green import urllib2
except ImportError:
    print 'eventlet is needed'
    exit()

init()

# default parameters
threads = 100
wait = 0.
randomNames = False
customdir = False


def randomUA(): 
    return 'Mozilla/{:.1f} (X{:.0f}; rv:{:.1f}) Firefox/{:.1f}'.format(random.random()*10., random.random()*100., random.random()*100., random.random()*100.)

def randomHexString(l=80): 
    return ''.join(random.choice('0123456789ABCDEF') for _ in xrange(l))

def fetchFiles(name, url):
    if not os.path.exists(name):
        time.sleep(random.random() * wait)
        opener = urllib2.build_opener()
        opener.addheaders = [
                             #('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                             #('Accept-Encoding', 'gzip, deflate'),
                             ('Connection', 'close'),
                             #('Proxy-Authorization', randomHexString()),
                             ('User-agent', randomUA())
                             ]
        try:
            r = opener.open(url)
            open(name, 'wb').write(r.read())
        except Exception as e:
            sys.stderr.write('\n\033[31m * Exception caught:  {}  {}  {}\033[0m\n'.format(type(e).__name__, url, name))
    else:
        sys.stderr.write('\n\033[31m * Already exists:  {}  {}\033[0m\n'.format(name, url))
    return name

if len(sys.argv) < 2:
    print 'You have to specify file with links'
    sys.exit()

for arg in sys.argv:
    if arg.startswith('--help'):
        print '''\
Concurrent downloader
    uses eventlet.GreenPool

Usage: {} [options] links-file

Options:
    --threads=int       Number of threads to download with (default={})
    --dir=str           Directory to download to (default=links-file)
    --randomnames       Give downloaded files random names (default={})
    --wait=float        Max time to wait between connections (default={})
'''.format(__name__, threads, randomNames, wait)
        exit()

    elif arg.startswith('--threads='):      threads = int(arg.split('=')[-1])
    elif arg.startswith('--dir='):          directory, customdir = arg.split('=')[-1], True
    elif arg.startswith('--randomnames'):   randomNames = True
    elif arg.startswith('--wait='):         wait = float(arg.split('=')[-1])

if not customdir: directory = sys.argv[-1].strip() + '_downloaded_files/'

with open(sys.argv[-1], 'r') as f:
    try:
        links = filter(bool, [x.strip() for x in f.readlines()])
    except IOError:
        sys.stderr.write('Cannot open file with links')
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
    t = raw_input('Continue anyway? y/n  ')
    if t in 'yY':
        sys.exit()

pool = eventlet.GreenPool(threads)
l = len(names)

filesGot = 0
start = time.time()
for name in pool.imap(fetchFiles, names, links):
    filesGot += 1
    sys.stdout.write('\r{} of {}'.format(filesGot, l))
    sys.stdout.flush()

print
finish = time.time()
print 'Execution time:', finish - start

