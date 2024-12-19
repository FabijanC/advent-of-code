package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

const HEIGHT = 103
const WIDTH = 101

type Pair struct {
	i, j int
}

type Robot struct {
	p, v Pair
}

func (r *Robot) move() {
	r.p.i = (r.p.i + r.v.i + HEIGHT) % HEIGHT
	r.p.j = (r.p.j + r.v.j + WIDTH) % WIDTH
}

func parsePair(s string) Pair {
	parts := strings.Split(s, ",")
	j, _ := strconv.Atoi(parts[0])
	i, _ := strconv.Atoi(parts[1])
	return Pair{i, j}
}

func printRobots(robots []Robot) {
	for i := 0; i <= HEIGHT; i++ {
		for j := 0; j <= WIDTH; j++ {
			currentPosition := Pair{i, j}
			robotCount := 0
			for i := range robots {
				if robots[i].p == currentPosition {
					robotCount++
				}
			}

			if robotCount == 0 {
				fmt.Print(".")
			} else {
				fmt.Print(robotCount)
			}
		}
		fmt.Println()
	}
}

func hashRobots(robots []Robot) int {
	h := 0
	for i := range robots {
		for _, v := range []int{robots[i].p.i, robots[i].p.j, robots[i].v.i, robots[i].v.j} {
			h = (h << 5) ^ (h >> 27) ^ v
		}
	}

	return h
}

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintf(os.Stderr, "Error: %s: <INPUT_FILE>", os.Args[0])
		os.Exit(1)
	}

	filePath := os.Args[1]
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: Cannot read %s", filePath)
	}

	bio := bufio.NewScanner(file)

	robots := []Robot{}
	for bio.Scan() {
		line := bio.Text()
		lineParts := strings.Split(line, " ")
		p := parsePair(lineParts[0][2:])
		v := parsePair(lineParts[1][2:])
		robots = append(robots, Robot{p, v})
	}

	hashToTime := map[int]int{}
	var period int
	for t := 1; true; t++ {
		h := hashRobots(robots)
		oldT, seen := hashToTime[h]
		if seen {
			period = t - oldT
			fmt.Println("Same configuration at:", oldT, "and", t)
			fmt.Println("Period:", period)
			break
		}
		hashToTime[h] = t

		for i := range robots {
			robots[i].move()
		}
	}

	stdinBio := bufio.NewScanner(os.Stdin)
	fmt.Println()
	for t := 1; t < period; t++ {
		for i := range robots {
			robots[i].move()
		}
		
		// value obtained after printing for each t and spotting (but missing) the tree
		if t > 7500 {
			fmt.Println("t:", t)
			printRobots(robots)
			fmt.Println()
			stdinBio.Scan() // wait for user to check printed content
		}
	}

}
