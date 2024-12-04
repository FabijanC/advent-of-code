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
		line_buff, _, err := bio.ReadLine()
		if err != nil {
			break
		}

		line := string(line_buff)
		symbols := strings.Split(line, "")
		grid = append(grid, symbols)
	}

	height := len(grid)
	width := len(grid[0])

	goal := []string{"X", "M", "A", "S"}
	match_count := 0

	// iterate through all 8 directions
	for di := -1; di <= 1; di++ {
		for dj := -1; dj <= 1; dj++ {
			if di == 0 && dj == 0 {
				continue
			}

			// iterate through all starting points
			for i := 0; i < height; i++ {
				for j := 0; j < width; j++ {
					string_matched := true
					for goal_i, goal_symbol := range goal {
						candidate_i := i + goal_i*di
						candidate_j := j + goal_i*dj
						if candidate_i < 0 ||
							candidate_i >= height ||
							candidate_j < 0 ||
							candidate_j >= width ||
							grid[candidate_i][candidate_j] != goal_symbol {
							string_matched = false
							break
						}
					}

					if string_matched {
						match_count++
					}
				}
			}
		}
	}

	fmt.Println(match_count)
}
