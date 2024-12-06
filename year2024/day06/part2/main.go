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

	line_i := 0
	var guard_start Point
	for scanner.Scan() {
		line := scanner.Text()
		grid = append(grid, line)

		candidate_j := strings.Index(line, "^")
		if candidate_j != -1 {
			guard_start = Point{i: line_i, j: candidate_j}
		}

		line_i++
	}

	height := len(grid)
	width := len(grid[0])

	new_obstacle_count := 0
	for obstacle_i := 0; obstacle_i < height; obstacle_i++ {
		for obstacle_j := 0; obstacle_j < width; obstacle_j++ {
			if grid[obstacle_i][obstacle_j] == OBSTACLE {
				continue
			}

			directed_guard := DirectedPoint{
				direction: Point{i: -1, j: 0}, // facing up
				position:  guard_start,
			}
			seen := make(map[DirectedPoint]bool)
			loop_found := false
			for {
				if _, present := seen[directed_guard]; present {
					loop_found = true
					break
				}
				seen[directed_guard] = true

				next_position := directed_guard.NextPosition()
				if next_position.i < 0 || next_position.i >= height || next_position.j < 0 || next_position.j >= width {
					break
				}

				if grid[next_position.i][next_position.j] == OBSTACLE || (next_position.i == obstacle_i && next_position.j == obstacle_j) {
					directed_guard.TurnRight()
				} else {
					directed_guard.position = next_position
				}
			}

			if loop_found {
				new_obstacle_count++
			}
		}
	}

	fmt.Println(new_obstacle_count)
}
