package main

import (
	"bufio"
	"fmt"
	"os"
)

const HEIGHT = 5
const WIDTH = 5

type Key = [WIDTH]byte
type Lock = [WIDTH]byte

const KEY_TOP = "....."
const KEY_BOTTOM = "#####"

const LOCK_TOP = "#####"
const LOCK_BOTTOM = "....."

const EMPTY = '.'
const FULL = '#'

func ReadBlock(bio *bufio.Scanner) [WIDTH]byte {
	arr := [WIDTH]byte{}

	for _ = range HEIGHT {
		bio.Scan()
		line := bio.Text()

		for i := range len(line) {
			if line[i] == FULL {
				arr[i]++
			}
		}
	}

	bio.Scan() // read remaining block line
	bio.Text()

	return arr
}

func main() {
	bio := bufio.NewScanner(os.Stdin)

	keys := []Key{}
	locks := []Lock{}

	for bio.Scan() {
		line := bio.Text()
		if line == KEY_TOP {
			key := ReadBlock(bio)
			keys = append(keys, key)
		} else if line == LOCK_TOP {
			lock := ReadBlock(bio)
			locks = append(locks, lock)
		} else {
			fmt.Println("Invalid schema top", line)
			os.Exit(1)
		}

		bio.Scan() // read remaining empty line
		bio.Text()
	}

	pairs := 0
	for _, key := range keys {
		for _, lock := range locks {
			fit := true
			for i := range WIDTH {
				if key[i]+lock[i] > HEIGHT {
					fit = false
					break
				}
			}

			if fit {
				pairs++
			}
		}
	}

	fmt.Println(pairs)
}
