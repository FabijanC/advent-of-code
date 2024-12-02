package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func abs(x int) int {
	if x > 0 {
		return x
	} else {
		return -x
	}
}

func is_safe(num_values []int) bool {
	diff := num_values[1] - num_values[0]
	abs_diff := abs(diff)
	expect_ascending := num_values[1] > num_values[0]
	safe := abs_diff >= 1 && abs_diff <= 3
	for i := 2; safe && i < len(num_values); i++ {
		diff := num_values[i] - num_values[i-1]
		ascending := diff > 0
		abs_diff = abs(diff)

		if !(ascending == expect_ascending && abs_diff >= 1 && abs_diff <= 3) {
			return false
		}
	}

	return safe
}

func remove_and_clone(slice []int, removable_i int) []int {
	modified_slice := make([]int, len(slice)-1)
	modified_slice_i := 0
	for i, element := range slice {
		if i == removable_i {
			continue
		}
		modified_slice[modified_slice_i] = element
		modified_slice_i++
	}

	return modified_slice
}

func main() {
	bio := bufio.NewReader(os.Stdin)

	safe_count := 0

	for {
		byte_line, _, err := bio.ReadLine()
		if err != nil {
			// no more input lines
			break
		}
		line := string(byte_line)
		str_values := strings.Split(line, " ")
		num_values := make([]int, len(str_values))
		for i, str_value := range str_values {
			num_value, _ := strconv.Atoi(str_value)
			num_values[i] = num_value
		}

		if is_safe(num_values) {
			safe_count++
		} else {
			for i := range len(num_values) {
				modified_num_values := remove_and_clone(num_values, i)
				if is_safe(modified_num_values) {
					safe_count++
					break
				}
			}
		}
	}

	fmt.Println(safe_count)
}
