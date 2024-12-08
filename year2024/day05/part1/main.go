package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	var lessThan [100][100]bool

	bio := bufio.NewReader(os.Stdin)
	for {
		buff, _, _ := bio.ReadLine()
		if len(buff) == 0 {
			// checking buff instead of err to account for the empty delimiter line
			break
		}

		line := string(buff)
		lineParts := strings.Split(line, "|")
		left, _ := strconv.Atoi(lineParts[0])
		right, _ := strconv.Atoi(lineParts[1])

		lessThan[left][right] = true
	}

	middleSum := 0
	for {
		buff, _, err := bio.ReadLine()
		if err != nil {
			break
		}

		line := string(buff)
		lineParts := strings.Split(line, ",")
		pages := make([]int, len(lineParts))
		for i, rawPage := range lineParts {
			page, _ := strconv.Atoi(rawPage)
			pages[i] = page
		}

		orderingCorrect := true
		for i := 0; orderingCorrect && i < len(pages); i++ {
			for j := i + 1; j < len(pages); j++ {
				if !lessThan[pages[i]][pages[j]] {
					orderingCorrect = false
					break
				}
			}
		}

		if orderingCorrect {
			middleSum += pages[len(pages)/2]
		}
	}

	fmt.Println(middleSum)
}
