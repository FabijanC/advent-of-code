#!/bin/bash

run() {
    if [ -z "$1" ]; then
        echo 1>&2 "Error: $FUNCNAME <PROGRAM>"
        return 1
    fi

    go build -o "bin/$1" "$1/main.go" && "bin/$1"
}
export run
