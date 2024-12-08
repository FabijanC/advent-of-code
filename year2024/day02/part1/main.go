package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func abs(x int) int {
	if x > 0 {
		return x
	} else {
		return -x
	}
}

func main() {
	bio := bufio.NewReader(os.Stdin)

	safeCount := 0

	for {
		byteLine, _, err := bio.ReadLine()
		if err != nil {
			// no more input lines
			break
		}
		line := string(byteLine)
		strValues := strings.Split(line, " ")
		numValues := make([]int, len(strValues))
		for i, s := range strValues {
			num, _ := strconv.Atoi(s)
			numValues[i] = num
		}

		diff := numValues[1] - numValues[0]
		absDiff := abs(diff)
		expectAscending := numValues[1] > numValues[0]
		safe := absDiff >= 1 && absDiff <= 3
		for i := 2; safe && i < len(numValues); i++ {
			diff := numValues[i] - numValues[i - 1]
			ascending := diff > 0
			absDiff = abs(diff)

			if !(ascending == expectAscending && absDiff >= 1 && absDiff <= 3) {
				safe = false
			}
		}

		if safe {
			safeCount++
		}
	}

	fmt.Println(safeCount)
}
