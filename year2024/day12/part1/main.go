package main

import (
	"bufio"
	"fmt"
	"os"
)

type Pair struct {
	i, j int
}

var DIRECTIONS = [...]Pair{{i: -1, j: 0}, {i: 1, j: 0}, {i: 0, j: -1}, {i: 0, j: 1}}

// Return (area, perimeter)
func measure(i, j int, symbol byte, field []string, seen [][]bool) (int, int) {
	if seen[i][j] {
		return 0, 0
	}
	seen[i][j] = true

	area, perimeter := 1, 0

	for _, d := range DIRECTIONS {
		ni, nj := i+d.i, j+d.j

		if ni < 0 || ni >= len(field) || nj < 0 || nj >= len(field[0]) {
			perimeter++
			continue
		}

		if field[ni][nj] != symbol {
			perimeter++
		} else {
			newArea, newPerimeter := measure(ni, nj, symbol, field, seen)
			area += newArea
			perimeter += newPerimeter
		}
	}

	return area, perimeter
}

func main() {
	bio := bufio.NewScanner(os.Stdin)

	field := []string{}
	seen := [][]bool{}
	for bio.Scan() {
		line := bio.Text()
		field = append(field, line)
		seen = append(seen, make([]bool, len(line)))
	}

	score := 0
	for i, row := range field {
		for j := 0; j < len(row); j++ {
			area, perimeter := measure(i, j, row[j], field, seen)
			score += area * perimeter
		}
	}

	fmt.Println(score)
}
