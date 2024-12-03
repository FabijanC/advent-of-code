package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
)

func main() {
	input_bytes, _ := io.ReadAll(os.Stdin)
	input_text := string(input_bytes)
	matcher, _ := regexp.Compile("mul\\((\\d+),(\\d+)\\)")
	instructions := matcher.FindAllStringSubmatch(input_text, -1)
	
	sum := 0
	for _, instruction := range instructions {
		if len(instruction) != 3 {
			panic("Invalid parse result")
		}

		val1, _ := strconv.Atoi(instruction[1])
		val2, _ := strconv.Atoi(instruction[2])
		sum += val1 * val2
	}

	fmt.Println(sum)
}
