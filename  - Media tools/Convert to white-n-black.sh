#!/bin/sh

for pic in $@
do
    convert $pic -colorspace gray wb-$pic
done
