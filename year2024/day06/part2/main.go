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

type DirectedPoint struct {
	direction Point
	position  Point
}

func (dp *DirectedPoint) TurnRight() {
	dp.direction.i, dp.direction.j = dp.direction.j, -dp.direction.i
}

func (dp *DirectedPoint) NextPosition() Point {
	return Point{
		i: dp.position.i + dp.direction.i,
		j: dp.position.j + dp.direction.j,
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var grid []string

	var guardStart Point
	for i := 0; scanner.Scan(); i++ {
		line := scanner.Text()
		grid = append(grid, line)

		j := strings.Index(line, "^")
		if j != -1 {
			guardStart = Point{i, j}
		}
	}

	height := len(grid)
	width := len(grid[0])

	newObstacleCount := 0
	for i := 0; i < height; i++ {
		for j := 0; j < width; j++ {
			if grid[i][j] == OBSTACLE {
				continue
			}
			newObstacle := Point{i, j}

			guard := DirectedPoint{
				direction: Point{i: -1, j: 0}, // facing up
				position:  guardStart,
			}
			seen := make(map[DirectedPoint]bool)
			loopFound := false
			for {
				if _, present := seen[guard]; present {
					loopFound = true
					break
				}
				seen[guard] = true

				nextPosition := guard.NextPosition()
				if nextPosition.i < 0 || nextPosition.i >= height || nextPosition.j < 0 || nextPosition.j >= width {
					break
				}

				if grid[nextPosition.i][nextPosition.j] == OBSTACLE || (nextPosition == newObstacle) {
					guard.TurnRight()
				} else {
					guard.position = nextPosition
				}
			}

			if loopFound {
				newObstacleCount++
			}
		}
	}

	fmt.Println(newObstacleCount)
}
