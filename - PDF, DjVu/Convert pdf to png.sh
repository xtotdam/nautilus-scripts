#!/bin/sh

FN=$1
FNOUT=${FN%.*}

#convert -verbose -density 450 -background white -alpha off -flatten $FN $FNOUT%d.png
convert -quality 100 -density 400x400 -background white -alpha off $FN $FNOUT-%03d.png
