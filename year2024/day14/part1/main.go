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

// const HEIGHT = 7
// const WIDTH = 11

const HEIGHT_HALF = HEIGHT / 2
const WIDTH_HALF = WIDTH / 2

const MAX_TIME = 100

type Pair struct {
	i, j int
}

type Quadrant struct {
	i, j bool
}

type Robot struct {
	p, v Pair
}

func (r *Robot) move() {
	r.p.i = (r.p.i + r.v.i + HEIGHT) % HEIGHT
	r.p.j = (r.p.j + r.v.j + WIDTH) % WIDTH
}

func (r *Robot) quadrant() *Quadrant {
	if r.p.i == HEIGHT_HALF || r.p.j == WIDTH_HALF {
		return nil
	}
	return &Quadrant{
		i: r.p.i > HEIGHT_HALF,
		j: r.p.j > WIDTH_HALF,
	}
}

func parsePair(s string) Pair {
	parts := strings.Split(s, ",")
	j, _ := strconv.Atoi(parts[0])
	i, _ := strconv.Atoi(parts[1])
	return Pair{i, j}
}

func main() {
	bio := bufio.NewScanner(os.Stdin)
	robots := []Robot{}
	for bio.Scan() {
		line := bio.Text()
		lineParts := strings.Split(line, " ")
		p := parsePair(lineParts[0][2:])
		v := parsePair(lineParts[1][2:])
		robots = append(robots, Robot{p, v})
	}

	for t := 0; t < MAX_TIME; t++ {
		for i := range robots {
			robots[i].move()
		}
	}

	quadrantCount := map[Quadrant]int{}
	for _, r := range robots {
		q := r.quadrant()
		if q != nil {
			quadrantCount[*q]++
		}
	}

	sol := 1
	for _, count := range quadrantCount {
		sol *= count
	}
	fmt.Println(sol)
}
