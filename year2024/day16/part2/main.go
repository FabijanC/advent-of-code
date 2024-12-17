package main

import (
	"bufio"
	"fmt"
	"os"
)

type Pair struct {
	i, j int
}

type DirectedPair struct {
	position, direction Pair
}

var RIGHT = Pair{i: 0, j: 1}
var LEFT = Pair{i: 0, j: -1}
var UP = Pair{i: -1, j: 0}
var DOWN = Pair{i: 1, j: 0}
var DIRECTIONS = []Pair{ RIGHT, LEFT, UP, DOWN }

func (p *Pair) move(direction Pair) Pair {
	return Pair{
		i: p.i + direction.i,
		j: p.j + direction.j,
	}
}

func turnRight(direction Pair) Pair {
	return Pair{
		i: direction.j,
		j: -direction.i,
	}
}

func turnLeft(direction Pair) Pair {
	return Pair{
		i: -direction.j,
		j: direction.i,
	}
}

const WALL = byte('#')
const END = byte('E')

func hasLeft(position, direction Pair, grid []string) bool {
	leftDirection := turnLeft(direction)
	leftPosition := Pair{
		i: position.i + leftDirection.i,
		j: position.j + leftDirection.j,
	}

	return grid[leftPosition.i][leftPosition.j] != WALL
}

const TURN_SCORE = 1000

type PathMap = map[DirectedPair][]DirectedPair

func search(position, direction Pair, score int, grid []string, scoreMemo map[DirectedPair]int, prevMemo PathMap, prevConfig DirectedPair) {
	if grid[position.i][position.j] == WALL {
		return
	}

	directedPair := DirectedPair{position, direction}
	oldScore, seen := scoreMemo[directedPair]
	if seen {
		if oldScore < score {
			return
		} else if oldScore == score {
			prevMemo[directedPair] = append(prevMemo[directedPair], prevConfig)
			return
		}
	}

	scoreMemo[directedPair] = score
	prevMemo[directedPair] = []DirectedPair{prevConfig}

	if grid[position.i][position.j] == END {
		return
	}

	leftDirection := turnLeft(direction)
	search(position, leftDirection, score+TURN_SCORE, grid, scoreMemo, prevMemo, prevConfig)

	rightDirection := turnRight(direction)
	search(position, rightDirection, score+TURN_SCORE, grid, scoreMemo, prevMemo, prevConfig)

	frontNeighbor := position.move(direction)
	search(frontNeighbor, direction, score+1, grid, scoreMemo, prevMemo, directedPair)
}

type Set = map[Pair]bool

func collectOptimalFields(directedPair, start DirectedPair, prevMemo PathMap, seenFields Set) {
	if seenFields[directedPair.position] == true {
		return
	}
	seenFields[directedPair.position] = true

	if directedPair == start {
		return
	}

	for _, neighbor := range prevMemo[directedPair] {
		collectOptimalFields(neighbor, start, prevMemo, seenFields)
	}
}

func main() {
	bio := bufio.NewScanner(os.Stdin)

	grid := []string{}
	for bio.Scan() {
		line := bio.Text()
		grid = append(grid, line)
	}

	startPosition := Pair{
		i: len(grid) - 2,
		j: 1,
	}

	scoreMemo := map[DirectedPair]int{}
	prevMemo := PathMap{}
	dummyPrev := DirectedPair{position: Pair{i: 0, j: 0}, direction: Pair{i: 0, j: 0}}
	search(startPosition, RIGHT, 0, grid, scoreMemo, prevMemo, dummyPrev)
	endField := Pair{i: 1, j: len(grid[0]) - 2}

	// among those entries in scoreMemo whose position is end, find the one with the smallest value
	minScore := 0
	minDirection := UP
	for _, direction := range DIRECTIONS {
		directedPair := DirectedPair{position: endField, direction: direction}
		score := scoreMemo[directedPair]
		if score < minScore {
			minScore = score
			minDirection = direction
		}
	}

	seenOptimalFields := Set{}
	collectOptimalFields(DirectedPair{position: endField, direction: minDirection}, DirectedPair{position: startPosition, direction: RIGHT}, prevMemo, seenOptimalFields)
	delete(seenOptimalFields, dummyPrev.direction)

	fmt.Println(len(seenOptimalFields))
}
