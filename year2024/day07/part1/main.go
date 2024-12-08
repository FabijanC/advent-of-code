package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func possible(goal int64, accumulated int64, material []int64, i int) bool {
	if accumulated > goal{
		return false
	}

	if accumulated == goal && i == len(material) {
		return true
	}

	if i >= len(material) {
		return false
	}

	return possible(goal, accumulated+material[i], material, i+1) ||
		possible(goal, accumulated*material[i], material, i+1)
}

// It could work with simply using int on the machine where this code was originally written
// (a 64-bit system), but to also support 32-bit architectures, int64 is explicitly used.
func toInt64(s string) (int64, error) {
	return strconv.ParseInt(s, 10, 64)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var calibrationResult int64 = 0
	for scanner.Scan() {
		line := scanner.Text()

		parts := strings.Split(line, ": ")
		goal, _ := toInt64(parts[0])

		materialJoint := parts[1]
		materialRaw := strings.Split(materialJoint, " ")
		material := make([]int64, len(materialRaw))
		for i, n := range materialRaw {
			material[i], _ = toInt64(n)
		}

		if possible(goal, material[0], material, 1) {
			calibrationResult += goal
		}
	}

	fmt.Println(calibrationResult)
}
