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

func search(position Pair, score int, corrupted [][]bool, memo [][]int) {
	if position.i < 0 || position.i >= SIZE || position.j < 0 || position.j >= SIZE || corrupted[position.i][position.j] {
		return
	}

	oldScore := memo[position.i][position.j]
	if oldScore <= score {
		return
	}
	memo[position.i][position.j] = score

	if position.i == SIZE-1 && position.j == SIZE-1 {
		return
	}

	for _, d := range []Pair{{i: 0, j: -1}, {i: 0, j: 1}, {i: -1, j: 0}, {i: 1, j: 0}} {
		search(Pair{
			i: position.i + d.i,
			j: position.j + d.j,
		}, score+1, corrupted, memo)
	}
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
	corrupted := make2d(SIZE, SIZE, false)

	bio := bufio.NewScanner(os.Stdin)
	for inputLines := 0; inputLines < 1024 && bio.Scan(); inputLines++ {
		line := bio.Text()
		lineParts := strings.Split(line, ",")

		// Each byte position is given as an X,Y coordinate, where X is the distance from the
		// left edge of your memory space and Y is the distance from the top edge of your memory space.
		j, _ := strconv.Atoi(lineParts[0])
		i, _ := strconv.Atoi(lineParts[1])
		corrupted[i][j] = true
	}

	memo := make2d(SIZE, SIZE, INFINITY)

	search(Pair{i: 0, j: 0}, 0, corrupted, memo)
	fmt.Println(memo[SIZE-1][SIZE-1])
}
