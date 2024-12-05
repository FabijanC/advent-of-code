package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	var less_than [100][100]bool

	bio := bufio.NewReader(os.Stdin)
	for {
		buff_line, _, _ := bio.ReadLine()
		if len(buff_line) == 0 {
			// checking buff_line instead of err to account for the empty delimiter line
			break
		}

		line := string(buff_line)
		line_parts := strings.Split(line, "|")
		left, _ := strconv.Atoi(line_parts[0])
		right, _ := strconv.Atoi(line_parts[1])

		less_than[left][right] = true
	}

	middle_sum := 0
	for {
		buff_line, _, err := bio.ReadLine()
		if err != nil {
			break
		}

		line := string(buff_line)
		line_parts := strings.Split(line, ",")
		pages := make([]int, len(line_parts))
		for i, raw_page := range line_parts {
			page, _ := strconv.Atoi(raw_page)
			pages[i] = page
		}

		ordering_correct := true
		for i := 0; ordering_correct && i < len(pages); i++ {
			for j := i + 1; j < len(pages); j++ {
				if !less_than[pages[i]][pages[j]] {
					ordering_correct = false
					break
				}
			}
		}

		if !ordering_correct {
			sort.Slice(pages, func(i, j int) bool {
				return less_than[pages[i]][pages[j]]
			})
			middle_sum += pages[len(pages) / 2]
		}
	}

	fmt.Println(middle_sum)
}
