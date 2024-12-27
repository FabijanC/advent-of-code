package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"slices"
	"strings"
)

type Wire = string
type GateType string

type Gate struct {
	input1, input2, output Wire
	operator               GateType
}

func (g *Gate) OtherInput(input Wire) Wire {
	if g.input1 == input {
		return g.input2
	}

	if g.input2 == input {
		return g.input1
	}

	panic("Invalid input wire")
}

type Signal bool

func parseWireValue(s string) Signal {
	switch s {
	case "0":
		return false
	case "1":
		return true
	default:
		panic("Invalid wire value: " + s)
	}
}

type Wires map[Wire]Signal
type OutputToGate map[Wire]*Gate

func calculateOutput(wire Wire, gates OutputToGate, wires Wires) Signal {
	wireOutput, known := wires[wire]
	if known {
		return wireOutput
	}

	gate := gates[wire]
	input1Value := calculateOutput(gate.input1, gates, wires)
	input2Value := calculateOutput(gate.input2, gates, wires)

	var outputValue Signal
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

func (gates OutputToGate) FindOutput(x, y Wire, operator GateType) (Wire, error) {
	outputs := gates.FindGates(x, y, operator, WILDCARD)

	if len(outputs) == 0 {
		return "", errors.New("Gate not present")
	}

	if len(outputs) > 1 {
		return "", errors.New("Too many gates found")
	}

	return outputs[0].output, nil
}

const WILDCARD = "ANY"

func operatorsMatch(o1, o2 GateType) bool {
	return o1 == WILDCARD || o2 == WILDCARD || o1 == o2
}

func wiresMatch(x, y Wire) bool {
	return x == WILDCARD || y == WILDCARD || x == y
}

func (gates OutputToGate) FindGates(x, y Wire, operator GateType, z Wire) []*Gate {
	outputs := []*Gate{}

	for _, gate := range gates {
		inputMatched := (wiresMatch(gate.input1, x) && wiresMatch(gate.input2, y)) || (wiresMatch(gate.input1, y) && wiresMatch(gate.input2, x))
		operatorsMatched := operatorsMatch(gate.operator, operator)
		outputMatched := wiresMatch(gate.output, z)
		if inputMatched && operatorsMatched && outputMatched {
			outputs = append(outputs, gate)
		}
	}

	return outputs
}

func (gate *Gate) String() string {
	return fmt.Sprintf("{%s %s %s -> %s}", gate.input1, gate.operator, gate.input2, gate.output)
}

type WirePair struct {
	w1, w2 Wire
}

// Check if x + y + c == z
// If ok, return new carry wire
// If not ok, return swappable wires
func checkFullAdder(x, y, cIn, z Wire, gates OutputToGate) (bool, Wire, *WirePair) {
	firstXor, err := gates.FindOutput(x, y, "XOR")
	if err != nil {
		panic("Should never be the case because only outputs are swapped")
	}

	nextZ, err := gates.FindOutput(firstXor, cIn, "XOR")
	if err != nil {
		alternativeGates := gates.FindGates(firstXor, WILDCARD, "XOR", z)
		if len(alternativeGates) == 1 {
			return false, "", &WirePair{cIn, alternativeGates[0].OtherInput(firstXor)}
		}

		alternativeGates = gates.FindGates(cIn, WILDCARD, "XOR", z)
		if len(alternativeGates) == 1 {
			return false, "", &WirePair{firstXor, alternativeGates[0].OtherInput(cIn)}
		}
	}

	if nextZ != z {
		return false, "", &WirePair{nextZ, z}
	}

	firstAnd, err := gates.FindOutput(x, y, "AND")
	if err != nil {
		// here and in subsequent if-branches, returning nil would result in nil-dereference,
		// but this is never done for the input.txt file in this directory
		return false, "", nil
	}

	secondAnd, err := gates.FindOutput(firstXor, cIn, "AND")
	if err != nil {
		return false, "", nil
	}

	cOut, err := gates.FindOutput(firstAnd, secondAnd, "OR")
	if err != nil {
		return false, "", nil
	}

	return true, cOut, nil
}

func NewWire(prefix byte, i int) Wire {
	return fmt.Sprintf("%c%02d", prefix, i)
}

func main() {
	bio := bufio.NewScanner(os.Stdin)

	// read wires
	for bio.Scan() {
		line := bio.Text()
		if len(line) == 0 {
			break
		}
	}

	// read gates
	gates := OutputToGate{}
	for bio.Scan() {
		line := bio.Text()

		gateParts := strings.Split(line, " -> ")
		inputParts := strings.Split(gateParts[0], " ")
		output := gateParts[1]

		gates[output] = &Gate{
			input1:   inputParts[0],
			operator: GateType(inputParts[1]),
			input2:   inputParts[2],
			output:   output,
		}
	}

	outputWires := Wires{}
	for outputWire := range gates {
		if outputWire[0] == 'z' {
			outputWires[outputWire] = true
		}
	}

	cIn, err := gates.FindOutput("x00", "y00", "AND")
	if err != nil {
		panic(err)
	}

	swappableWires := []Wire{}

	// most significant output bit doesn't exist in input
	for i := 1; i < len(outputWires)-1; {
		xIn := NewWire('x', i)
		yIn := NewWire('y', i)
		zIn := NewWire('z', i)
		ok, nextCin, swappable := checkFullAdder(xIn, yIn, cIn, zIn, gates)
		if ok {
			cIn = nextCin
			i++ // move on to next output wire
		} else {
			swappableWires = append(swappableWires, swappable.w1)
			swappableWires = append(swappableWires, swappable.w2)
			gates[swappable.w1], gates[swappable.w2] = gates[swappable.w2], gates[swappable.w1]
			gates[swappable.w1].output, gates[swappable.w2].output = gates[swappable.w2].output, gates[swappable.w1].output
		}
	}

	highestOutputWire := NewWire('z', len(outputWires)-1)
	if highestOutputWire != cIn {
		panic("Most significant output bit should be the last carry")
	}

	slices.Sort(swappableWires)
	fmt.Println(strings.Join(swappableWires, ","))
}
