from sys import path
from os.path import dirname
path.append(dirname(path[0]))
from intcode import Intcode
import sys
import copy

computer = Intcode(sys.argv[1])
stored = copy.deepcopy(computer)
sol = 0
for i in range(50):
    for j in range(50):
        computer.put([i,j])
        output = computer.run()
        sol += output == 1
        computer = copy.deepcopy(stored)
print(sol)