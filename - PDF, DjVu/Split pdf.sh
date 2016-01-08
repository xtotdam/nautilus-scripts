#!/bin/sh

IN=$1
NAME=${IN%.*}

mv "$1" "$NAME.old.pdf"
python2 "/home/xtotdam/.local/share/nautilus/scripts/- Split pages/un2up.py" <"$NAME.old.pdf" >"$NAME.pdf"
