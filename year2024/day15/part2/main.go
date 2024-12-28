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
const BOX_LEFT = '['
const BOX_RIGHT = ']'

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

func (g Grid) double() Grid {
	newG := Grid{}
	for i := 0; i < len(g); i++ {
		newRow := []byte{}
		for j := 0; j < len(g[0]); j++ {
			switch g[i][j] {
			case WALL:
				newRow = append(newRow, WALL)
				newRow = append(newRow, WALL)
			case BOX:
				newRow = append(newRow, BOX_LEFT)
				newRow = append(newRow, BOX_RIGHT)
			case EMPTY:
				newRow = append(newRow, EMPTY)
				newRow = append(newRow, EMPTY)
			case ROBOT:
				newRow = append(newRow, ROBOT)
				newRow = append(newRow, EMPTY)
			}
		}
		newG = append(newG, newRow)
	}

	return newG
}

func (g Grid) get(p *Pair) byte {
	return g[p.i][p.j]
}

func (g Grid) set(p *Pair, symbol byte) {
	g[p.i][p.j] = symbol
}

func (g Grid) getMovablePiecesHorizontal(position, direction Pair, movablePieces map[Pair]byte) error {
	for {
		currSymbol := g.get(&position)
		if currSymbol == EMPTY {
			return nil
		}

		if currSymbol == WALL {
			return errors.New("Wall reached")
		}

		movablePieces[position] = currSymbol

		position = position.neighbor(&direction)
	}
}

func (g Grid) getMovablePiecesVertical(position, direction Pair, movablePieces map[Pair]byte) error {
	// check if already seen
	_, seen := movablePieces[position]
	if seen {
		return nil
	}

	currSymbol := g.get(&position)
	switch currSymbol {
	case WALL:
		return errors.New("Wall reached")
	case EMPTY:
		return nil
	case BOX_LEFT:
		movablePieces[position] = currSymbol
		err := g.getMovablePieces(position.neighbor(&direction), direction, movablePieces)
		if err != nil {
			return err
		}

		otherBoxPartDir := SYMBOL_TO_PAIR[RIGHT]
		otherBoxPartPos := position.neighbor(&otherBoxPartDir)
		movablePieces[otherBoxPartPos] = BOX_RIGHT
		return g.getMovablePieces(otherBoxPartPos.neighbor(&direction), direction, movablePieces)
	case BOX_RIGHT:
		movablePieces[position] = currSymbol
		err := g.getMovablePieces(position.neighbor(&direction), direction, movablePieces)
		if err != nil {
			return err
		}

		otherBoxPartDir := SYMBOL_TO_PAIR[LEFT]
		otherBoxPartPos := position.neighbor(&otherBoxPartDir)
		movablePieces[otherBoxPartPos] = BOX_LEFT
		return g.getMovablePieces(otherBoxPartPos.neighbor(&direction), direction, movablePieces)
	default:
		panic("Should never be here")
	}
}

func (g Grid) getMovablePieces(position, direction Pair, movablePieces map[Pair]byte) error {
	// if moving horizontally, no recursive calls
	if direction == SYMBOL_TO_PAIR[LEFT] || direction == SYMBOL_TO_PAIR[RIGHT] {
		return g.getMovablePiecesHorizontal(position, direction, movablePieces)
	}

	// otherwise moving vertically, requires recursion
	return g.getMovablePiecesVertical(position, direction, movablePieces)
}

func (r *Robot) move(dirSymbol byte) {
	dir := SYMBOL_TO_PAIR[dirSymbol]

	firstNeighbor := r.position.neighbor(&dir)
	firstNeighborSymbol := r.grid.get(&firstNeighbor)
	switch firstNeighborSymbol {
	case EMPTY:
		r.position = firstNeighbor
	case BOX_LEFT, BOX_RIGHT:
		// find first empty field
		movablePieces := map[Pair]byte{}
		err := r.grid.getMovablePieces(firstNeighbor, dir, movablePieces)
		if err != nil {
			return
		}

		for p := range movablePieces {
			r.grid.set(&p, EMPTY)
		}

		for p := range movablePieces {
			nextPos := p.neighbor(&dir)
			r.grid.set(&nextPos, movablePieces[p])
		}

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

	grid = grid.double()

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
			if grid[i][j] == BOX_LEFT {
				sol += i*100 + j
			}
		}
	}

	fmt.Println(sol)
}
