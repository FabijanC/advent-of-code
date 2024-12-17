package main

import (
	"fmt"
)

// The program
var EXPECTED_OUTPUT = []int{2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 6, 5, 5, 3, 0}

func main() {
	candidate := 136904921145256
	for initialA := candidate - 500_000_000; initialA < candidate+500_000_000; initialA++ {
		a, b, c := initialA, 0, 0

		outputIndex := 0
		outputOk := true

		for {
			// The program transformed into more human-readable instructions
			b = a & 0b111
			b ^= 5
			c = a >> b
			b ^= 6
			a >>= 3
			b ^= c

			digit := b & 0b111
			if outputIndex > len(EXPECTED_OUTPUT) || digit != EXPECTED_OUTPUT[outputIndex] {
				outputOk = false
				break
			} else {
				outputIndex++
			}

			if a == 0 {
				break
			}
		}

		if outputOk && outputIndex == len(EXPECTED_OUTPUT) {
			fmt.Println("Solution:", initialA)
			break
		}
	}
}
