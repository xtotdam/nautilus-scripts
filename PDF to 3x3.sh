#!/bin/bash

IN="$1"
OUT="${IN::-4}-3x3.pdf"
TEMP="pdfjamtemp-3x3.pdf"

pdfnup --nup 3x3 --frame true $IN --outfile $TEMP
pdfcrop $TEMP $OUT
rm -vf $TEMP
notify-send "PDF 3x3" "$IN converted to $OUT"
