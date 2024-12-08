package main

import (
	"bufio"
	"fmt"
	"os"
)

type Point struct{ i, j int }

func (p *Point) Move(di, dj int) {
	p.i += di
	p.j += dj
}

const EMPTY = '.'

func contains(grid []string, p *Point) bool {
	return p.i >= 0 && p.i < len(grid) && p.j >= 0 && p.j < len(grid[0])
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	grid := []string{}
	for scanner.Scan() {
		line := scanner.Text()
		grid = append(grid, line)
	}

	// byte and rune are functionally equivalent for this purpose - all symbols are single bytes
	antennas := make(map[rune][]Point)
	for i, row := range grid {
		for j, symbol := range row {
			if symbol == EMPTY {
				continue
			}

			antennas[symbol] = append(antennas[symbol], Point{i, j})
		}
	}

	hasAntinode := make(map[Point]bool)
	for _, locations := range antennas {
		for i, location1 := range locations {
			for j, location2 := range locations {
				if i == j {
					continue
				}

				di := location1.i - location2.i
				dj := location1.j - location2.j

				for antinode := location1; contains(grid, &antinode); antinode.Move(di, dj) {
					hasAntinode[antinode] = true
				}

				for antinode := location2; contains(grid, &antinode); antinode.Move(-di, -dj) {
					hasAntinode[antinode] = true
				}
			}
		}
	}

	fmt.Println(len(hasAntinode))
}
