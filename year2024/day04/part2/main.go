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

	matchCount := 0

	// iterate through all potential X middles (letter A)
	for i := 1; i < height-1; i++ {
		for j := 1; j < width-1; j++ {
			if grid[i][j] != "A" {
				continue
			}

			// concatenate corners
			corners := strings.Join([]string{
				grid[i-1][j-1],
				grid[i-1][j+1],
				grid[i+1][j-1],
				grid[i+1][j+1]},
				"")

			if corners == "MMSS" || corners == "MSMS" || corners == "SSMM" || corners == "SMSM" {
				matchCount++
			}

		}
	}

	fmt.Println(matchCount)
}
