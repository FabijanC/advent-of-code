"""Day 1, part 1"""

import sys


def main():
    """Main"""
    l1, l2 = [], []
    for line in sys.stdin:
        el1, el2 = [int(x) for x in line.split()]
        l1.append(el1)
        l2.append(el2)

    l1.sort()
    l2.sort()

    assert len(l1) == len(l2)
    distance_sum = 0
    for el1, el2 in zip(l1, l2):
        distance_sum += abs(el1 - el2)

    print(distance_sum)


main()
