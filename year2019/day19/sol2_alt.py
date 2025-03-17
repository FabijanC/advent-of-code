from sys import path
from os.path import dirname
path.append(dirname(path[0]))
from intcode import Intcode
import sys
import copy
import math

SQUARE_DIST = 99

class Dummy:
    def __init__(self, file_path):
        with open(file_path) as f:
            self.content = f.read().split("\n")
    
    def put(self, pos):
        self.pos = pos
    
    def run(self):
        return int(self.content[self.pos[0]][self.pos[1]] == '#')

#computer = Dummy("out.txt")
computer = Intcode(sys.argv[1])
stored = copy.deepcopy(computer)
size = int(sys.argv[2])
init_i, init_j = 8, 10

upper_i, upper_j = init_i, init_j
upper = set([(upper_i, upper_j)])
for _ in range(size):
    computer = copy.deepcopy(stored)
    computer.put([upper_i, upper_j+1])
    if computer.run() == 1:
        upper_j += 1
    else:
        upper_i += 1
    upper.add((upper_i, upper_j))

lower_i, lower_j = init_i, init_j
for _ in range(size):
    computer = copy.deepcopy(stored)
    computer.put([lower_i+1, lower_j])
    if computer.run() == 1:
        lower_i += 1
    else:
        computer = copy.deepcopy(stored)
        computer.put([lower_i, lower_j+1])
        assert computer.run() == 1
        lower_j += 1
    
    for delta in range(10):
        if (lower_i-SQUARE_DIST, lower_j+SQUARE_DIST+delta) in upper:
            print(lower_i-SQUARE_DIST, lower_j, delta)
            exit()

    # upper.add((upper_i, upper_j))

    # if (lower_i-size, lower_j+size) in upper:
    #     print(lower_i-size, lower_j)
    #     print(lower_j*10000 + lower_i-size)
    #     break
