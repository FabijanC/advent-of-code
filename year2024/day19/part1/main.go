package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func possible(design string, designIndex int, material map[string]bool) bool {
	if designIndex >= len(design) {
		return true
	}

	prefix := ""
	for ; designIndex < len(design); designIndex++ {
		prefix += string(design[designIndex])

		_, prefixInMaterial := material[prefix]
		if prefixInMaterial && possible(design, designIndex+1, material) {
			return true
		}
	}

	return false
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

	count := 0
	for bio.Scan() {
		design := bio.Text()
		if possible(design, 0, material) {
			count++
		}
	}

	fmt.Println(count)
}
