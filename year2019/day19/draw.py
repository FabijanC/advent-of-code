from sys import path
from os.path import dirname
path.append(dirname(path[0]))
from intcode import Intcode
import sys
import copy

def is_beam(i, j):
    computer = copy.deepcopy(stored)
    computer.put([i, lower_j])
    return computer.run()

stored = Intcode(sys.argv[1])
size = int(sys.argv[2])
init_i = 8
lower_j, upper_j = 9, 11
lines = []
i = init_i
while i < size:
    print("i < size", i)
    while not is_beam(i, lower_j):
        print("not")
        lower_j += 1
    while is_beam(i, upper_j):
        print("is", upper_j)
        upper_j += 1
    upper_j -= 1

    lines.append((lower_j, upper_j))
    i += 1

for i in range(init_i):
    print("."*size)

for lower_j, upper_j in lines:
    print("."*lower_j, "#"*(upper_j-lower_j+1), "."*(size-upper_j-1), sep="")
