package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

const MOD = 16777216
const STEPS = 2000

func nextSecret(secret int) int {
	secret = ((secret * 64) ^ secret) % MOD
	secret = ((secret / 32) ^ secret) % MOD
	secret = ((secret * 2048) ^ secret) % MOD
	return secret
}

func main() {
	bio := bufio.NewScanner(os.Stdin)

	sol := 0
	for bio.Scan() {
		line := bio.Text()
		secret, _ := strconv.Atoi(line)
		for i := 0; i < STEPS; i++ {
			secret = nextSecret(secret)
		}
		sol += secret
	}

	fmt.Println(sol)
}
