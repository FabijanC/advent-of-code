from sys import path
from os.path import dirname
path.append(dirname(path[0]))
from intcode import Intcode
import sys

computer = Intcode(file_name=sys.argv[1])

area = [[]]
while True:
    output = computer.run()
    if output is None:
        break
    output = chr(output)
    if output == '\n':
        area.append([])
    else:
        area[-1].append(output)

while len(area[-1]) == 0:
    area.pop()

sol = 0
height = len(area)
width = len(area[0])
for i in range(1, height-1):
    for j in range(1, width-1):
        if area[i][j] == '#' and area[i-1][j] == '#' and area[i+1][j] == '#' and area[i][j-1] == '#' and area[i][j+1] == '#':
            sol += i*j
print(sol)