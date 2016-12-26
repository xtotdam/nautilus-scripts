#!/bin/bash

IN="$1"
OUT="${IN::-4}-4x1.pdf"
TEMP="pdfjamtemp-4x1.pdf"

pdfnup --nup 4x1 --frame true $IN --outfile $TEMP
pdfcrop $TEMP $OUT
rm -vf $TEMP
notify-send "PDF 4x1" "$IN converted to $OUT"
