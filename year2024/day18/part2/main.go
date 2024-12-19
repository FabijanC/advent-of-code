package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Pair struct {
	i, j int
}

const SIZE = 71
const INFINITY = 100_000_000_000

func endReachable(position Pair, t int, seen [][]bool, corruptionTimes [][]int) bool {
	if position.i < 0 || position.i >= SIZE || position.j < 0 || position.j >= SIZE ||
		t >= corruptionTimes[position.i][position.j] {
		return false
	}

	if position.i == SIZE-1 && position.j == SIZE-1 {
		return true
	}

	if seen[position.i][position.j] {
		return false
	}
	seen[position.i][position.j] = true

	for _, d := range []Pair{{i: 0, j: -1}, {i: 0, j: 1}, {i: -1, j: 0}, {i: 1, j: 0}} {
		if endReachable(Pair{
			i: position.i + d.i,
			j: position.j + d.j,
		}, t, seen, corruptionTimes) {
			return true
		}
	}

	return false
}

func make2d[T any](rows, cols int, value T) [][]T {
	m := make([][]T, rows)

	for i := 0; i < rows; i++ {
		row := make([]T, cols)
		for j := range row {
			row[j] = value
		}
		m[i] = row
	}

	return m
}

func main() {
	corruptionTimes := make2d(SIZE, SIZE, INFINITY)
	corruptedPositions := []Pair{}

	bio := bufio.NewScanner(os.Stdin)
	for t := 0; bio.Scan(); t++ {
		line := bio.Text()
		lineParts := strings.Split(line, ",")

		// Each byte position is given as an X,Y coordinate, where X is the distance from the
		// left edge of your memory space and Y is the distance from the top edge of your memory space.
		j, _ := strconv.Atoi(lineParts[0])
		i, _ := strconv.Atoi(lineParts[1])
		corruptionTimes[i][j] = t
		corruptedPositions = append(corruptedPositions, Pair{i, j})
	}

	// searching for smallest `t` for which end is NOT reachable
	tLow, tHigh := 0, 10000
	for tLow < tHigh {
		t := (tLow + tHigh) / 2
		seen := make2d(SIZE, SIZE, false)
		if endReachable(Pair{i: 0, j: 0}, t, seen, corruptionTimes) {
			tLow = t + 1
		} else {
			tHigh = t
		}
	}

	blockingByte := corruptedPositions[tLow]
	fmt.Printf("End blocked at t=%d with byte %d,%d\n", tLow, blockingByte.j, blockingByte.i)
}
