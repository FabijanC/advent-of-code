package main

import (
	"bufio"
	"fmt"
	"math/rand"
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

func programToInt(program []int) int {
	n := 0
	for i := len(program) - 1; i >= 0; i-- {
		n = n*10 + program[i]
	}
	return n
}

func absDiff(a, b int) int {
	if a > b {
		return a - b
	} else {
		return b - a
	}
}

func main() {
	initialRegisters := Registers{}

	bio := bufio.NewScanner(os.Stdin)
	for r := A; r <= C; r++ {
		bio.Scan()
		line := bio.Text()

		lineParts := strings.Split(line, ": ")
		value, _ := strconv.Atoi(lineParts[1])
		initialRegisters[r] = value
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

	nearestOutputNum := 0
	expectedOutputNum := programToInt(program)

	// iterate over initial values for register A
	tooLow := 20000000000000
	tooHigh := 200000000000000
	for {
		initialA := tooLow + rand.Intn(tooHigh-tooLow)
		registers := Registers{
			A: initialA,
			B: initialRegisters[B],
			C: initialRegisters[C],
		}

		output := []int{}
	programLoop:
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
				digit := comboOperand & MASK
				output = append(output, digit)
				if len(output) > len(program) {
					break programLoop
				}
			case BDV:
				registers[B] = registers[A] >> comboOperand
			case CDV:
				registers[C] = registers[A] >> comboOperand
			default:
				panic("Invalid opcode")
			}

			pointer += 2
		}

		outputNum := programToInt(output)
		if outputNum == expectedOutputNum {
			fmt.Println("Solution:", initialA)
			break
		} else if absDiff(outputNum, expectedOutputNum) < absDiff(nearestOutputNum, expectedOutputNum) {
			fmt.Printf("New best. A=%d, output=%d, output/A=%.10f\n", initialA, output, float64(outputNum)/float64(expectedOutputNum))
			nearestOutputNum = outputNum
		}
	}
}
