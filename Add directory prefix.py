#!/usr/bin/python2

import os

place = os.getcwd()

dir = place.split(os.sep)[-1]

for f in os.listdir(place):
    os.rename(place+os.sep+f, place+os.sep+dir+'_'+f)
