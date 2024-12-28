package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
)

type Pair struct {
	i, j int
}
type Grid [][]byte
type Robot struct {
	grid     Grid
	position Pair
}

const UP = '^'
const DOWN = 'v'
const RIGHT = '>'
const LEFT = '<'

var SYMBOL_TO_PAIR = map[byte]Pair{
	UP:    {i: -1, j: 0},
	DOWN:  {i: 1, j: 0},
	LEFT:  {i: 0, j: -1},
	RIGHT: {i: 0, j: 1},
}

const ROBOT = '@'
const EMPTY = '.'
const WALL = '#'
const BOX = 'O'

func (p Pair) neighbor(dir *Pair) Pair {
	return Pair{
		i: p.i + dir.i,
		j: p.j + dir.j,
	}
}

func (p *Pair) backward() Pair {
	return Pair{
		i: -p.i,
		j: -p.j,
	}
}

func (g Grid) find(b byte) Pair {
	for i := 0; i < len(g); i++ {
		for j := 0; j < len(g[0]); j++ {
			if g[i][j] == b {
				return Pair{i, j}
			}
		}
	}

	panic("Byte not present in grid: " + string(b))
}

func (g Grid) get(p *Pair) byte {
	return g[p.i][p.j]
}

func (g Grid) set(p *Pair, symbol byte) {
	g[p.i][p.j] = symbol
}

// if box cannot move, error is not nil
func (g Grid) findBoxDestination(position, direction Pair) (Pair, error) {
	for g.get(&position) == BOX {
		position = position.neighbor(&direction)
	}

	if g.get(&position) == EMPTY {
		return position, nil
	}

	return Pair{}, errors.New("Box immovable")
}

func (r *Robot) move(dirSymbol byte) {
	dir := SYMBOL_TO_PAIR[dirSymbol]

	firstNeighbor := r.position.neighbor(&dir)
	switch r.grid.get(&firstNeighbor) {
	case EMPTY:
		r.position = firstNeighbor
	case BOX:
		// find first empty field
		firstEmpty, err := r.grid.findBoxDestination(firstNeighbor, dir)
		if err != nil {
			return
		}

		r.grid.set(&firstEmpty, BOX)
		r.grid.set(&firstNeighbor, EMPTY)
		r.position = firstNeighbor

	default:
		// immovable object
	}
}

func main() {
	bio := bufio.NewScanner(os.Stdin)

	grid := Grid{}
	for bio.Scan() {
		line := bio.Text()

		if len(line) == 0 {
			break
		}

		grid = append(grid, []byte(line))
	}

	robotPosition := grid.find(ROBOT)
	grid.set(&robotPosition, EMPTY)
	r := Robot{
		grid:     grid,
		position: robotPosition,
	}

	directions := ""
	for bio.Scan() {
		directions += bio.Text()
	}

	for i := 0; i < len(directions); i++ {
		r.move(directions[i])
	}

	sol := 0
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid[0]); j++ {
			if grid[i][j] == BOX {
				sol += i*100 + j
			}
		}
	}

	fmt.Println(sol)
}
