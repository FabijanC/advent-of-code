package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

const OBSTACLE = '#'

type Point struct {
	i int
	j int
}

func (p *Point) NextPosition(direction *Point) Point {
	return Point{
		i: p.i + direction.i,
		j: p.j + direction.j,
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var grid []string

	line_i := 0
	var guard Point
	for scanner.Scan() {
		line := scanner.Text()
		grid = append(grid, line)

		candidate_j := strings.Index(line, "^")
		if candidate_j != -1 {
			guard = Point{i: line_i, j: candidate_j}
		}

		line_i++
	}

	height := len(grid)
	width := len(grid[0])

	direction := Point{i: -1, j: 0} // facing up
	visited := make(map[Point]bool)

	for {
		visited[guard] = true

		next_position := guard.NextPosition(&direction)
		if next_position.i < 0 || next_position.i >= height || next_position.j < 0 || next_position.j >= width {
			break
		}

		if grid[next_position.i][next_position.j] == OBSTACLE {
			// turn right
			direction.i, direction.j = direction.j, -direction.i
		} else {
			guard = next_position
		}
	}

	fmt.Println(len(visited))
}
