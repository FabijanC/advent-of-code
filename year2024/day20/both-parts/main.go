package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

const START = 'S'
const END = 'E'
const EMPTY = '.'
const WALL = '#'

const INFINITY = 1e12

var UP = Point{i: -1, j: 0}
var DOWN = Point{i: 1, j: 0}
var LEFT = Point{i: 0, j: -1}
var RIGHT = Point{i: 0, j: 1}
var DIRECTIONS = []Point{UP, DOWN, LEFT, RIGHT}

func abs(x int) int {
	if x < 0 {
		return -x
	}

	return x
}

type Grid = [][]byte

type Point struct{ i, j int }

func (p *Point) neighbor(direction Point) Point {
	return Point{i: p.i + direction.i, j: p.j + direction.j}
}

func (p *Point) inside(grid Grid) bool {
	return p.i >= 0 && p.i < len(grid) && p.j >= 0 && p.j < len(grid[0])
}

func (p *Point) distance(other *Point) int {
	return abs(p.i-other.i) + abs(p.j-other.j)
}

type Cheat struct {
	entrance, exit Point
}

func (c *Cheat) distance() int {
	return c.entrance.distance(&c.exit)
}

type Memo = map[Point]int

func search(p Point, t int, grid Grid, memo Memo) {
	if !p.inside(grid) || grid[p.i][p.j] == WALL {
		return
	}

	oldT, seen := memo[p]
	if seen && oldT <= t {
		return
	}
	memo[p] = t

	if grid[p.i][p.j] == END {
		return
	}

	for _, d := range DIRECTIONS {
		neighbor := p.neighbor(d)
		search(neighbor, t+1, grid, memo)
	}
}

func findByte(grid Grid, b byte) Point {
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid[0]); j++ {
			if grid[i][j] == b {
				return Point{i, j}
			}
		}
	}

	panic("No byte in the grid is equal to " + string(b))
}

func setByte(grid Grid, p Point, b byte) {
	grid[p.i][p.j] = b
}

func countDesirableCheats(pointToTime Memo, maxCheatDistance int, minimumSave int) int {
	count := 0
	for entrance, entranceTime := range pointToTime {
		for exit, exitTime := range pointToTime {
			cheatDistance := entrance.distance(&exit)
			physicalDistance := exitTime - entranceTime
			if cheatDistance <= maxCheatDistance && physicalDistance - cheatDistance >= minimumSave {
				count++
			}
		}
	}

	return count
}
func invalidInputExit(program string) {
	fmt.Fprintf(os.Stderr, "Input error! Expected: %s <MAX_CHEAT_DURATION> <MIN_EXPECTED_IMPROVEMENT>", program)
	os.Exit(1)
}

func parseInput(args []string) (int, int) {
	if len(args) != 3 {
		invalidInputExit(args[0])
	}

	maxCheatDuration, err := strconv.Atoi(args[1])
	if err != nil {
		invalidInputExit(args[0])
	}

	minImprovement, err := strconv.Atoi(args[2])
	if err != nil {
		invalidInputExit(args[0])
	}

	return maxCheatDuration, minImprovement
}

func main() {
	maxCheatDuration, minImprovement := parseInput(os.Args)
	bio := bufio.NewScanner(os.Stdin)

	grid := Grid{}

	for bio.Scan() {
		line := bio.Text()
		grid = append(grid, []byte(line))
	}

	start := findByte(grid, START)

	pointToTime := Memo{}
	search(start, 0, grid, pointToTime)

	improvements := countDesirableCheats(pointToTime, maxCheatDuration, minImprovement)
	fmt.Println("Cheats leading to desired improvement:", improvements)
}
