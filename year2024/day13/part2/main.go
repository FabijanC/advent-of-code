package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func extract(line string, r *regexp.Regexp) (int, int) {
	matches := r.FindAllStringSubmatch(line, -1)
	if len(matches) != 2 {
		panic("Invalid line: " + line)
	}

	value1, _ := strconv.Atoi(matches[0][0])
	value2, _ := strconv.Atoi(matches[1][0])

	return value1, value2
}

func check(vectorX, vectorY int, targetX, targetY int) bool {
	return targetX/vectorX == targetY/vectorY && targetX%vectorX == 0 && targetY%vectorY == 0
}

func main() {
	r, _ := regexp.Compile("\\d+")

	priceA := 3
	priceB := 1

	totalPrice := 0

	bio := bufio.NewScanner(os.Stdin)
	for bio.Scan() {
		line := bio.Text()
		if len(line) == 0 {
			// skip empty lines
			continue
		}

		xA, yA := extract(line, r)

		bio.Scan()
		line = bio.Text()
		xB, yB := extract(line, r)

		bio.Scan()
		line = bio.Text()
		xP, yP := extract(line, r)
		delta := 10000000000000
		xP += delta
		yP += delta

		// x_a * a + x_b * b = x_p
		// y_a * a + y_b * b = y_p
		// -----------------------
		// x_a * a = x_p - x_b * b
		// a = (x_p - x_b * b) / x_a
		// y_a * (x_p - x_b * b) / x_a + y_b * b = y_p
		// x_p / x_a - x_b * b / x_a + y_b * b / y_a = y_p / y_a
		// b * (-x_b / x_a + y_b / y_a) = y_p / y_a - x_p / x_a
		// b * [ (-x_b * y_a + y_b * x_a) / (x_a * y_a) ] = (y_p * x_a - x_p * y_a) / (y_a * x_a)
		// b = (y_p * x_a - x_p * y_a) / (-x_b * y_a + y_b * x_a)

		numeratorB := yP*xA - xP*yA
		denominatorB := -xB*yA + yB*xA

		if denominatorB == 0 {
			// vectors are colinear

			// first try out the cheaper one - button B
			if check(xB, yB, xP, yP) {
				totalPrice += priceB * xP / xB
			} else if check(xA, yA, xP, yP) {
				totalPrice += priceA * xP / xA
			}
		} else if numeratorB%denominatorB == 0 {
			b := numeratorB / denominatorB

			numeratorA := (xP - xB*b)
			denominatorA := xA

			if numeratorA%denominatorA == 0 {
				a := (xP - xB*b) / xA
				totalPrice += a*priceA + b*priceB
			}

		}
	}

	fmt.Println(totalPrice)
}
