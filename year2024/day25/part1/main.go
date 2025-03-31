package main

import (
	"bufio"
	"fmt"
	"os"
)

const HEIGHT = 5
const WIDTH = 5

type Mechanism = [WIDTH]byte
type Key = Mechanism
type Lock = Mechanism

const KEY_TOP = "....."
const LOCK_TOP = "#####"
const FULL = '#'

func parseBlock(bio *bufio.Scanner) Mechanism {
	mechanism := Mechanism{}

	for range HEIGHT {
		bio.Scan()
		line := bio.Text()

		for i := range len(line) {
			if line[i] == FULL {
				mechanism[i]++
			}
		}
	}

	bio.Scan() // read remaining block line
	bio.Text()

	return mechanism
}

func main() {
	bio := bufio.NewScanner(os.Stdin)

	keys := []Key{}
	locks := []Lock{}

	for bio.Scan() {
		line := bio.Text()
		mechanism := parseBlock(bio)

		if line == KEY_TOP {
			keys = append(keys, mechanism)
		} else if line == LOCK_TOP {
			locks = append(locks, mechanism)
		} else {
			fmt.Fprintln(os.Stderr, "Invalid block top:", line)
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
