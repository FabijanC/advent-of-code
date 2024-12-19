package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func countWays(design string, designIndex int, material map[string]bool, memo map[string]int) int {
	if designIndex >= len(design) {
		return 1
	}

	rest := design[designIndex:]
	oldCount, seen := memo[rest]
	if seen {
		return oldCount
	}

	count := 0
	prefix := ""
	for ; designIndex < len(design); designIndex++ {
		prefix += string(design[designIndex])

		_, prefixInMaterial := material[prefix]
		if prefixInMaterial {
			ways := countWays(design, designIndex+1, material, memo)
			count += ways
		}
	}

	memo[rest] = count
	return count
}

func main() {
	bio := bufio.NewScanner(os.Stdin)

	bio.Scan()
	line := bio.Text()

	towels := strings.Split(line, ", ")
	material := map[string]bool{}
	for _, towel := range towels {
		material[towel] = true
	}

	bio.Scan()
	bio.Text() // skip empty line

	memo := map[string]int{}
	count := 0
	for bio.Scan() {
		design := bio.Text()
		count += countWays(design, 0, material, memo)
	}

	fmt.Println(count)
}
