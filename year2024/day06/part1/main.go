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

	var guard Point
	for i := 0; scanner.Scan(); i++ {
		line := scanner.Text()
		grid = append(grid, line)

		j := strings.Index(line, "^")
		if j != -1 {
			guard = Point{i, j}
		}
	}

	height := len(grid)
	width := len(grid[0])

	direction := Point{i: -1, j: 0} // facing up
	visited := make(map[Point]bool)

	for {
		visited[guard] = true

		next := guard.NextPosition(&direction)
		if next.i < 0 || next.i >= height || next.j < 0 || next.j >= width {
			break
		}

		if grid[next.i][next.j] == OBSTACLE {
			// turn right
			direction.i, direction.j = direction.j, -direction.i
		} else {
			guard = next
		}
	}

	fmt.Println(len(visited))
}
