package main

import (
	"bufio"
	"fmt"
	"os"
)

type Pair struct {
	i, j int
}

var RIGHT = Pair{i: 0, j: 1}

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

func search(position, direction Pair, score int, grid []string, memo map[Pair]int) {
	if grid[position.i][position.j] == WALL {
		return
	}

	oldScore, seen := memo[position]
	if seen && oldScore <= score {
		return
	}

	memo[position] = score

	if grid[position.i][position.j] == END {
		return
	}

	leftDirection := turnLeft(direction)
	leftNeighbor := position.move(leftDirection)
	search(leftNeighbor, leftDirection, score+TURN_SCORE+1, grid, memo)

	rightDirection := turnRight(direction)
	rightNeighbor := position.move(rightDirection)
	search(rightNeighbor, rightDirection, score+TURN_SCORE+1, grid, memo)

	frontNeighbor := position.move(direction)
	search(frontNeighbor, direction, score+1, grid, memo)
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

	memo := map[Pair]int{}
	search(startPosition, RIGHT, 0, grid, memo)

	endField := Pair{i: 1, j: len(grid[0]) - 2}
	fmt.Println(memo[endField])
}
