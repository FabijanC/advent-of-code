package main

import (
	"fmt"
)

func main() {
	var l1 []int
	freq2 := make(map[int]int)
	for {
		var el1, el2 int
		_, err := fmt.Scanf("%d %d", &el1, &el2)
		if err != nil {
			break
		}

		l1 = append(l1, el1)
		freq2[el2]++
	}

	score := 0
	for _, el1 := range l1 {
		score += el1 * freq2[el1]
	}

	fmt.Println(score)
}
