#!/bin/bash

# Put selected pictures to single GIF

R=$(date +%Y%d%m%H%M%S%N)
FN=$(basename "$PWD")

convert -delay 10 $@ -loop 0 $FN-$R.gif
