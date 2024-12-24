package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strings"
)

type Node = string

type NodePair struct {
	n1, n2 Node
}

type NodeTriplet struct {
	n1, n2, n3 Node
}

func NewNodeTriplet(n1, n2, n3 Node) NodeTriplet {
	nodes := []Node{n1, n2, n3}
	slices.Sort(nodes)
	return NodeTriplet{nodes[0], nodes[1], nodes[2]}
}

type Graph map[NodePair]bool

func main() {
	bio := bufio.NewScanner(os.Stdin)

	graph := Graph{}
	nodes := map[Node]bool{}

	for bio.Scan() {
		line := bio.Text()
		computers := strings.Split(line, "-")
		c1, c2 := computers[0], computers[1]
		nodes[c1] = true
		nodes[c2] = true
		graph[NodePair{c1, c2}] = true
		graph[NodePair{c2, c1}] = true
	}

	triplets := map[NodeTriplet]bool{}
	for n1 := range nodes {
		for n2 := range nodes {
			for n3 := range nodes {
				if n1[0] != 't' && n2[0] != 't' && n3[0] != 't' {
					continue
				}

				if graph[NodePair{n1, n2}] && graph[NodePair{n1, n3}] && graph[NodePair{n2, n3}] {
					triplets[NewNodeTriplet(n1, n2, n3)] = true
				}
			}
		}
	}

	fmt.Println(len(triplets))
}
