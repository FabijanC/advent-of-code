#!/bin/bash

run() {
    if [ -z "$1" ]; then
        echo 1>&2 "Error: $FUNCNAME <PROGRAM>"
        return 1
    fi

    program="$1"
    shift # to support passing args to the program

    go build -o "bin/$program" "$program/main.go" && "bin/$program" $@
}
export run
