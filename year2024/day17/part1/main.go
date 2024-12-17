package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// registers
const A = 4
const B = 5
const C = 6

// opcodes
const ADV = 0
const BXL = 1
const BST = 2
const JNZ = 3
const BXC = 4
const OUT = 5
const BDV = 6
const CDV = 7

const MASK = 0b111 // for mod 8 operations

type Registers = map[int]int

func Combo(val int, registers Registers) int {
	if val <= 3 {
		return val
	} else {
		return registers[val]
	}
}

func main() {
	registers := Registers{A: 0, B: 0, C: 0}

	bio := bufio.NewScanner(os.Stdin)
	for r := A; r <= C; r++ {
		bio.Scan()
		line := bio.Text()

		lineParts := strings.Split(line, ": ")
		value, _ := strconv.Atoi(lineParts[1])
		registers[r] = value
	}

	// empty line
	bio.Scan()
	bio.Text()

	bio.Scan()
	programLine := bio.Text()
	programRaw := strings.Split(programLine, ": ")[1]
	programStrings := strings.Split(programRaw, ",")

	program := make([]int, len(programStrings))
	for i, s := range programStrings {
		n, _ := strconv.Atoi(s)
		program[i] = n
	}

	output := []int{}
	for pointer := 0; pointer >= 0 && pointer < len(program); {
		instruction := program[pointer]
		operand := program[pointer+1]
		comboOperand := Combo(operand, registers)

		switch instruction {
		case ADV:
			registers[A] >>= comboOperand
		case BXL:
			registers[B] ^= operand
		case BST:
			registers[B] = comboOperand & MASK
		case JNZ:
			if registers[A] == 0 {
				// do nothing
			} else {
				pointer = operand
				continue
			}
		case BXC:
			registers[B] ^= registers[C]
		case OUT:
			output = append(output, comboOperand&MASK)
		case BDV:
			registers[B] = registers[A] >> comboOperand
		case CDV:
			registers[C] = registers[A] >> comboOperand
		default:
			panic("Invalid opcode")
		}

		pointer += 2
	}

	if len(output) > 0 {
		fmt.Print(output[0])
	}
	for i := 1; i < len(output); i++ {
		fmt.Print(",", output[i])
	}
	fmt.Println()
}
