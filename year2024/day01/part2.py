"""Day 1, part 2"""

import sys
from collections import defaultdict


def main():
    """Main"""
    l1, freq2 = [], defaultdict(int)
    for line in sys.stdin:
        el1, el2 = [int(x) for x in line.split()]
        l1.append(el1)
        freq2[el2] += 1

    similarity_score = 0
    for el in l1:
        similarity_score += el * freq2[el]

    print(similarity_score)


main()
