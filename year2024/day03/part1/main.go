package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
)

func main() {
	inputBytes, _ := io.ReadAll(os.Stdin)
	inputText := string(inputBytes)
	matcher, _ := regexp.Compile("mul\\((\\d+),(\\d+)\\)")
	instructions := matcher.FindAllStringSubmatch(inputText, -1)
	
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
