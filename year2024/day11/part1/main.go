package main

import (
	"bufio"
	"container/list"
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

func main() {
	bio := bufio.NewScanner(os.Stdin)
	bio.Scan()
	line := bio.Text()

	stones := list.New()

	for _, raw_stone := range strings.Split(line, " ") {
		stone_value, _ := strconv.Atoi(raw_stone)
		stones.PushBack(stone_value)
	}

	for blink := 0; blink < 25; blink++ {
		for s := stones.Front(); s != nil; s = s.Next() {
			value := s.Value.(int)
			if s.Value == 0 {
				s.Value = 1
			} else if numLength(value)%2 == 0 {
				leftValue, rightValue := splitNum(value)
				s.Value = leftValue
				s = stones.InsertAfter(rightValue, s)
			} else {
				s.Value = value * 2024
			}
		}
	}

	fmt.Println(stones.Len())
}
