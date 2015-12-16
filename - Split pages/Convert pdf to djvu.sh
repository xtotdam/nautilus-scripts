#!/bin/sh

IN=$1
pdf2djvu -j0 $1 > ${IN%.*}.djvu
