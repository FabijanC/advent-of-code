package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func main() {
	inputBytes, _ := io.ReadAll(os.Stdin)
	inputText := string(inputBytes)
	matcher, _ := regexp.Compile("mul\\((\\d+),(\\d+)\\)|do\\(\\)|don't\\(\\)")
	instructions := matcher.FindAllStringSubmatch(inputText, -1)

	sum := 0
	enabled := true
	for _, instruction := range instructions {
		if strings.HasPrefix(instruction[0], "do(") {
			enabled = true
		} else if strings.HasPrefix(instruction[0], "don't(") {
			enabled = false
		} else if strings.HasPrefix(instruction[0], "mul(") && enabled {
			val1, _ := strconv.Atoi(instruction[1])
			val2, _ := strconv.Atoi(instruction[2])
			sum += val1 * val2
		}
	}

	fmt.Println(sum)
}
