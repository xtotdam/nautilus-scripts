#!/bin/sh

IN=$1
NAME=${IN%.*}
RND=`date | md5sum | tr -d ' -'`

ddjvu -format=pdf $1 $RND.pdf
mv $1 $NAME.old.djvu
python2 "/home/xtotdam/.local/share/nautilus/scripts/- Split pages/un2up.py" <$RND.pdf >$RND.temp.pdf
#rm -v $RND.pdf
pdf2djvu --lossy -j0 $RND.temp.pdf >$NAME.djvu
#rm -v $RND.temp.pdf
