#!/usr/bin/python2

import sys
import os

summary = sys.argv[0]
details = '\n'.join(sys.argv[1:])

os.system('notify-send "{0}" "cwd = {1}\nargs = \n{2}"'.format(summary, os.getcwd(), details))
