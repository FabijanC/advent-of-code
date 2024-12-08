package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	bio := bufio.NewReader(os.Stdin)

	var grid [][]string
	for {
		buff, _, err := bio.ReadLine()
		if err != nil {
			break
		}

		line := string(buff)
		symbols := strings.Split(line, "")
		grid = append(grid, symbols)
	}

	height := len(grid)
	width := len(grid[0])

	goal := []string{"X", "M", "A", "S"}
	matchCount := 0

	// iterate through all 8 directions
	for di := -1; di <= 1; di++ {
		for dj := -1; dj <= 1; dj++ {
			if di == 0 && dj == 0 {
				continue
			}

			// iterate through all starting points
			for i := 0; i < height; i++ {
				for j := 0; j < width; j++ {
					matched := true
					for goalIndex, goalSymbol := range goal {
						// candidate cooridnates
						ci := i + goalIndex*di
						cj := j + goalIndex*dj
						if ci < 0 ||
							ci >= height ||
							cj < 0 ||
							cj >= width ||
							grid[ci][cj] != goalSymbol {
							matched = false
							break
						}
					}

					if matched {
						matchCount++
					}
				}
			}
		}
	}

	fmt.Println(matchCount)
}
