package main

import (
	"fmt"
	"slices"
)

func main() {
	var l1, l2 []int
	for {
		var el1, el2 int
		_, err := fmt.Scanf("%d %d", &el1, &el2)
		if err != nil {
			break
		}

		l1 = append(l1, el1)
		l2 = append(l2, el2)
	}

	slices.Sort(l1)
	slices.Sort(l2)

	sum := 0
	for i, el1 := range l1 {
		el2 := l2[i]
		if el1 > el2 {
			sum += el1 - el2
		} else {
			sum += el2 - el1
		}
	}

	fmt.Println(sum)
}
