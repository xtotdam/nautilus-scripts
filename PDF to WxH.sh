#!/bin/bash

# Works with single file only
# Usable for reading from wide screens / learning from presentations

WXH=$(zenity --title "PDF WxH" --text "Enter WxH (default 3x3)\nPress Cancel to abort" --entry)
if [ $? -eq 1 ]; then echo "Aborting..."; exit; fi
if [ -z "$WXH" ]; then WXH="3x3"; fi

IN="$1"
OUT="${IN::-4}-$WXH.pdf"
TEMP=".temp-$WXH-1e9b14ba3d319d55b08b1da614ffcf3d.pdf"

pdfnup --nup $WXH --frame true "$IN" --outfile "$TEMP"
pdfcrop "$TEMP" "$OUT"
rm -vf "$TEMP"
notify-send "PDF WxH" "$IN converted to $OUT"
