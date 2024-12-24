package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

const MOD = 16777216
const STEPS = 2000
const CHANGE_LEN = 4

type Quad [4]int

func sliceToQuad(slice []int) Quad {
	if len(slice) != CHANGE_LEN {
		panic("Invalid slice length")
	}

	q := Quad{}
	for i := 0; i < CHANGE_LEN; i++ {
		q[i] = slice[i]
	}

	return q
}

func nextSecret(secret int) int {
	secret = ((secret * 64) ^ secret) % MOD
	secret = ((secret / 32) ^ secret) % MOD
	secret = ((secret * 2048) ^ secret) % MOD
	return secret
}

type Buyer struct {
	generatedPrices, changes [STEPS]int
}

type QuadMemo map[Quad]struct{}

func addChangeQuads(changes [STEPS]int, memo QuadMemo) {
	for i := 0; i < len(changes)-CHANGE_LEN; i++ {
		q := sliceToQuad(changes[i : i+CHANGE_LEN])
		memo[q] = struct{}{}
	}
}

func main() {
	bio := bufio.NewScanner(os.Stdin)

	buyers := []Buyer{}

	for bio.Scan() {
		line := bio.Text()
		secret, _ := strconv.Atoi(line)
		buyer := Buyer{}
		for i := 0; i < STEPS; i++ {
			prevSecret := secret
			secret = nextSecret(secret)
			buyer.generatedPrices[i] = secret % 10
			buyer.changes[i] = (secret % 10) - (prevSecret % 10)
		}

		buyers = append(buyers, buyer)
	}

	changeQuads := QuadMemo{}
	for i := 0; i < len(buyers); i++ {
		addChangeQuads(buyers[i].changes, changeQuads)
	}

	maxScore := 0
	for changeQuad := range changeQuads {
		score := 0
		for i := 0; i < len(buyers); i++ {
			for j := 0; j < len(buyers[i].changes)-CHANGE_LEN; j++ {
				actualChange := sliceToQuad(buyers[i].changes[j : j+CHANGE_LEN])
				if changeQuad == actualChange {
					addablePrice := buyers[i].generatedPrices[j+CHANGE_LEN-1]
					score += addablePrice
					break
				}
			}
		}

		if score > maxScore {
			maxScore = score
		}
	}

	fmt.Println(maxScore)
}
