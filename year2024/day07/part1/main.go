package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func is_possible(goal int64, accumulated int64, material []int64, material_i int) bool {
	if accumulated > goal{
		return false
	}

	if accumulated == goal && material_i == len(material) {
		return true
	}

	if material_i >= len(material) {
		return false
	}

	return is_possible(goal, accumulated+material[material_i], material, material_i+1) ||
		is_possible(goal, accumulated*material[material_i], material, material_i+1)
}

// It could work with simply using int on the machine where this code was originally written
// (a 64-bit system), but to also support 32-bit architectures, int64 is explicitly used.
func to_int64(s string) (int64, error) {
	return strconv.ParseInt(s, 10, 64)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var calibration_result int64 = 0
	for scanner.Scan() {
		line := scanner.Text()

		parts := strings.Split(line, ": ")
		goal, _ := to_int64(parts[0])

		material_joint := parts[1]
		material_raw := strings.Split(material_joint, " ")
		material := make([]int64, len(material_raw))
		for i, n := range material_raw {
			material[i], _ = to_int64(n)
		}

		if is_possible(goal, material[0], material, 1) {
			calibration_result += goal
		}
	}

	fmt.Println(calibration_result)
}
