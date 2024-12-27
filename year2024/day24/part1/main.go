package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Wire = string

type Gate struct {
	input1, input2 Wire
	operator               string
}

func parseWireValue(s string) bool {
	switch s {
	case "0":
		return false
	case "1":
		return true
	default:
		panic("Invalid wire value: " + s)
	}
}

type Wires map[Wire]bool
type GateOutputs map[Wire]*Gate

func calculateOutput(wire Wire, gateOutputs GateOutputs, wires Wires) bool {
	wireOutput, known := wires[wire]
	if known {
		return wireOutput
	}

	gate := gateOutputs[wire]
	input1Value := calculateOutput(gate.input1, gateOutputs, wires)
	input2Value := calculateOutput(gate.input2, gateOutputs, wires)

	var outputValue bool
	switch gate.operator {
	case "AND":
		outputValue = input1Value && input2Value
	case "OR":
		outputValue = input1Value || input2Value
	case "XOR":
		outputValue = input1Value != input2Value
	default:
		panic("Invalid operator: " + gate.operator)
	}

	wires[wire] = outputValue
	return outputValue
}

func main() {
	bio := bufio.NewScanner(os.Stdin)

	// read wires
	wires := map[Wire]bool{}
	for bio.Scan() {
		line := bio.Text()
		if len(line) == 0 {
			break
		}
		wireParts := strings.Split(line, ": ")
		wires[wireParts[0]] = parseWireValue(wireParts[1])
	}

	// read gates
	gateOutputs := GateOutputs{}
	for bio.Scan() {
		line := bio.Text()

		gateParts := strings.Split(line, " -> ")
		inputParts := strings.Split(gateParts[0], " ")
		output := gateParts[1]

		gateOutputs[output] = &Gate{
			input1:   inputParts[0],
			operator: inputParts[1],
			input2:   inputParts[2],
		}
	}

	zWires := map[Wire]bool{}
	for outputWire := range gateOutputs {
		if outputWire[0] == 'z' {
			zWires[outputWire] = calculateOutput(outputWire, gateOutputs, wires)
		}
	}

	// convert binary to decimal
	outputNumber := 0
	zWiresCount := len(zWires)
	for i := zWiresCount - 1; i >= 0; i-- {
		zWire := fmt.Sprintf("z%02d", i)

		outputNumber <<= 1
		if zWires[zWire] {
			outputNumber |= 1
		}
	}

	fmt.Println(outputNumber)
}
