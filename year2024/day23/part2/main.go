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

type Graph map[NodePair]bool

type Clique map[Node]bool

func (c Clique) contains(candidateNode Node, graph Graph) bool {
	for memberNode := range c {
		if !graph[NodePair{memberNode, candidateNode}] {
			return false
		}
	}
	return true
}

type NodeSet map[Node]bool

func initCliques(nodes NodeSet) []Clique {
	cliques := []Clique{}
	for node := range nodes {
		cliques = append(cliques, Clique{node: true})
	}

	return cliques
}

func getMaximumClique(nodes NodeSet, graph Graph) Clique {
	cliques := initCliques(nodes)

	for node := range nodes {
		for i := 0; i < len(cliques); i++ {
			if cliques[i].contains(node, graph) {
				cliques[i][node] = true
			}
		}
	}

	maxCliqueIndex := 0
	for i := 1; i < len(cliques); i++ {
		if len(cliques[i]) > len(cliques[maxCliqueIndex]) {
			maxCliqueIndex = i
		}
	}

	return cliques[maxCliqueIndex]
}

func (c Clique) getPassword() string {
	nodes := []string{}
	for n := range c {
		nodes = append(nodes, n)
	}

	slices.Sort(nodes)
	return strings.Join(nodes, ",")
}

func main() {
	bio := bufio.NewScanner(os.Stdin)

	graph := Graph{}
	nodeSet := map[Node]bool{}

	for bio.Scan() {
		line := bio.Text()
		computers := strings.Split(line, "-")
		c1, c2 := computers[0], computers[1]
		nodeSet[c1] = true
		nodeSet[c2] = true
		graph[NodePair{c1, c2}] = true
		graph[NodePair{c2, c1}] = true
	}

	maximumClique := getMaximumClique(nodeSet, graph)
	fmt.Println(maximumClique.getPassword())
}
