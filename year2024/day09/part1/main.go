package main

import (
	"bufio"
	"fmt"
	"os"
)

const EMPTY = -1

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	line := scanner.Text()

	disk := []int{}

	fileId := 0
	for i := 0; i < len(line); i++ {
		n := int(line[i]) - int('0')

		var currentId int
		if i%2 == 0 {
			// file block
			currentId = fileId
			fileId++
		} else {
			// empty block
			currentId = EMPTY
		}

		for j := 0; j < n; j++ {
			disk = append(disk, currentId)
		}
	}

	frontIndex := 0
	backIndex := len(disk) - 1

	for {
		// find empty space from front
		for frontIndex < len(disk) && disk[frontIndex] != EMPTY {
			frontIndex++
		}

		// find occupied space from back
		for backIndex >= 0 && disk[backIndex] == EMPTY {
			backIndex--
		}

		if frontIndex >= len(disk) || backIndex < 0 || frontIndex > backIndex {
			break
		}

		disk[frontIndex] = disk[backIndex]
		disk[backIndex] = EMPTY
	}

	checksum := 0
	for i := 0; i < len(disk); i++ {
		if disk[i] == EMPTY {
			continue
		}
		checksum += i * disk[i]
	}

	fmt.Println(checksum)
}
