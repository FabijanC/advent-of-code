#!/bin/bash

if [ ! -z "$1" ]; then
    DAY="$1"
else
    # defaults to today
    DAY=$(date +%d) # zero prefixed
fi

daydir="day$DAY"

mkdir -p "$daydir"

code -r "$daydir/"{part1,part2}"/main.go"
code -r "$daydir/"{input.txt,sample.txt}

. load_commands.sh

cd "$daydir"
