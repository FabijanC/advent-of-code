package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func numLength(n int) int {
	// to properly handle 0, though for this specific task it's not needed due to the 0->1 rule
	if n < 10 {
		return 1
	}

	length := 0
	for n > 0 {
		n /= 10
		length++
	}

	return length
}

func splitNum(n int) (int, int) {
	digits := []int{}
	for n > 0 {
		digits = append(digits, n%10)
		n /= 10
	}

	length := len(digits)
	// [len-1, len-2, ..., 3, 2, 1, 0]

	left := 0
	right := 0
	for i := 0; i < length/2; i++ {
		left = left*10 + digits[length-i-1]
		right = right*10 + digits[length/2-i-1]
	}

	return left, right
}

type Config struct {
	stone          int
	remainingSteps int
}

var memo = make(map[Config]int)

func count(stone, remainingSteps int) int {
	c := Config{stone, remainingSteps}
	old, has := memo[c]
	if has {
		return old
	}

	if remainingSteps == 0 {
		return 1
	}

	if stone == 0 {
		memo[c] = count(1, remainingSteps-1)
	} else if numLength(stone)%2 == 0 {
		leftStone, rightStone := splitNum(stone)
		memo[c] = count(leftStone, remainingSteps-1) + count(rightStone, remainingSteps-1)
	} else {
		memo[c] = count(stone*2024, remainingSteps-1)
	}

	return memo[c]
}

func main() {
	bio := bufio.NewScanner(os.Stdin)
	bio.Scan()
	line := bio.Text()

	stoneCount := 0
	for _, rawStone := range strings.Split(line, " ") {
		stone, _ := strconv.Atoi(rawStone)
		stoneCount += count(stone, 75)
	}

	fmt.Println(stoneCount)
}
