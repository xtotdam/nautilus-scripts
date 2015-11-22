#!/bin/bash

LINK=$(xclip -selection clipboard -o)

wget "$LINK"
