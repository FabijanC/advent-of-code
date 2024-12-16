package main

import (
	"bufio"
	"fmt"
	"os"
)

type Pair struct {
	i, j int
}

func (p *Pair) turnRight() {
	p.i, p.j = p.j, -p.i
}

func (p *Pair) turnLeft() {
	p.i, p.j = -p.j, p.i
}

type Set = map[Pair]bool

func contains(s Set, p Pair) bool {
	_, seen := s[p]
	return seen
}

var UP = Pair{i: -1, j: 0}
var DOWN = Pair{i: 1, j: 0}
var RIGHT = Pair{i: 0, j: 1}
var LEFT = Pair{i: 0, j: -1}
var CARDINAL_DIRECTIONS = []Pair{UP, DOWN, LEFT, RIGHT}
var EIGHT_DIRECTIONS = []Pair{UP, DOWN, LEFT, RIGHT, {i: -1, j: -1}, {i: 1, j: 1}, {i: -1, j: 1}, {i: 1, j: -1}}

type Searcher struct {
	position          Pair
	emptyDirection    Pair
	movementDirection Pair
}

func (s *Searcher) moveForward() {
	s.position.i += s.movementDirection.i
	s.position.j += s.movementDirection.j
}

func (s *Searcher) moveBack() {
	s.position.i -= s.movementDirection.i
	s.position.j -= s.movementDirection.j
}

func (s *Searcher) expectedEmptyPosition() Pair {
	return Pair{
		i: s.position.i + s.emptyDirection.i,
		j: s.position.j + s.emptyDirection.j,
	}
}

func (s *Searcher) turnLeft() {
	s.movementDirection.turnLeft()
	s.emptyDirection.turnLeft()
}

func (s *Searcher) turnRight() {
	s.movementDirection.turnRight()
	s.emptyDirection.turnRight()
}

// clockwise
func (s *Searcher) calculateOuterPerimeter(areaTiles Set) int {
	startingSearcher := *s
	perimeter := 0

	for {
		s.moveForward()

		if contains(areaTiles, s.position) {
			if contains(areaTiles, s.expectedEmptyPosition()) {
				s.turnLeft()
				s.moveForward()
				perimeter++
			} else {
				// ok, move on
			}
		} else {
			s.moveBack()
			s.turnRight()
			perimeter++
		}

		if *s == startingSearcher {
			break
		}
	}

	return perimeter
}

/*
Searches in eight directions to cover cases like:
xxx
x.x
xx.
Otherwise, the central tile is used in enclosed area perimeter calculation
*/
func collectOutsideArea(areaTiles Set, field []string) Set {
	outside := make(Set)
	seen := seenGrid(len(field), len(field[0]))

	for i := 0; i < len(field); i++ {
		for _, j := range []int{0, len(field[0]) - 1} {
			position := Pair{i, j}
			if !contains(areaTiles, position) && !seen[i][j] {
				predicate := func(p Pair) bool { return !contains(areaTiles, p) }
				collectTiles(position, predicate, EIGHT_DIRECTIONS, field, seen, outside)
			}
		}
	}

	for _, i := range []int{0, len(field) - 1} {
		for j := 0; j < len(field[0]); j++ {
			position := Pair{i, j}
			if !contains(areaTiles, position) && !seen[i][j] {
				predicate := func(p Pair) bool { return !contains(areaTiles, p) }
				collectTiles(position, predicate, EIGHT_DIRECTIONS, field, seen, outside)
			}
		}
	}

	return outside
}

func collectEnclosedArea(areaTiles Set, outsideTiles Set, field []string) []Set {
	seen := seenGrid(len(field), len(field[0]))

	enclosedAreas := []Set{}
	for i := 0; i < len(field); i++ {
		for j := 0; j < len(field[0]); j++ {
			position := Pair{i, j}
			if seen[i][j] || contains(areaTiles, position) || contains(outsideTiles, position) {
				continue
			}

			enclosedArea := make(Set)
			predicate := func(p Pair) bool { return !contains(areaTiles, p) }
			collectTiles(position, predicate, CARDINAL_DIRECTIONS, field, seen, enclosedArea)
			enclosedAreas = append(enclosedAreas, enclosedArea)
		}
	}

	return enclosedAreas
}

type PositionPredicate func(Pair) bool

// Populate `tiles` with positions at which `field` is satisfies `predicate`.
func collectTiles(position Pair, predicate PositionPredicate, directions []Pair, field []string, seen [][]bool, tiles Set) {
	if _, seen := tiles[position]; seen {
		return
	}

	seen[position.i][position.j] = true
	tiles[position] = true

	for _, d := range directions {
		nextPosition := Pair{i: position.i + d.i, j: position.j + d.j}
		if nextPosition.i < 0 || nextPosition.i >= len(field) || nextPosition.j < 0 || nextPosition.j >= len(field[0]) {
			continue
		}

		if !predicate(nextPosition) {
			continue
		}

		collectTiles(nextPosition, predicate, directions, field, seen, tiles)
	}
}

func seenGrid(rows, cols int) [][]bool {
	seen := [][]bool{}
	for i := 0; i < rows; i++ {
		seen = append(seen, make([]bool, cols))
	}
	return seen
}

// Returns a tile in an upper left corner of any kind
func findStartingTile(tiles Set) Pair {
	for p := range tiles {
		found := true
		for _, neighborDirection := range []Pair{LEFT, UP} {
			neighbor := Pair{i: p.i + neighborDirection.i, j: p.j + neighborDirection.j}
			if contains(tiles, neighbor) {
				found = false
				break
			}

		}

		// if no neighbors left or up in the same area - we have the starting tile
		if found {
			return p
		}
	}

	panic("No starting tile")
}

func main() {
	bio := bufio.NewScanner(os.Stdin)

	field := []string{}
	for bio.Scan() {
		line := bio.Text()
		field = append(field, line)
	}

	seen := seenGrid(len(field), len(field[0]))
	score := 0
	for i, row := range field {
		for j := 0; j < len(row); j++ {
			if seen[i][j] {
				continue
			}

			areaTiles := make(Set)
			predicate := func(p Pair) bool { return field[p.i][p.j] == field[i][j] }
			collectTiles(Pair{i, j}, predicate, CARDINAL_DIRECTIONS, field, seen, areaTiles)

			searcher := Searcher{
				position:          Pair{i, j},
				emptyDirection:    UP,
				movementDirection: RIGHT,
			}

			outerPerimeter := searcher.calculateOuterPerimeter(areaTiles)

			outsideArea := collectOutsideArea(areaTiles, field)
			enclosedAreas := collectEnclosedArea(areaTiles, outsideArea, field)
			innerPerimeter := 0
			for _, enclosedArea := range enclosedAreas {
				innerSearcher := Searcher{
					position:          findStartingTile(enclosedArea),
					emptyDirection:    UP,
					movementDirection: RIGHT,
				}
				innerPerimeter += innerSearcher.calculateOuterPerimeter(enclosedArea)
			}

			area := len(areaTiles)
			score += area * (outerPerimeter + innerPerimeter)
		}
	}

	fmt.Println(score)
}
