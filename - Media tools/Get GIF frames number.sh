#!/bin/bash

notify-send $1 $(identify $1 | wc -l)
