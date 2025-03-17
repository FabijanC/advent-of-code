from sys import path
from os.path import dirname
path.append(dirname(path[0]))
from intcode import Intcode
import copy
import sys

INF = int(1e9)

WALL = 0
SPACE = 1
OXYGEN_SOURCE = 2
kind2char = {WALL: '#', SPACE: ' ', OXYGEN_SOURCE: 'O', None: '?'}
movements = [(1, -1, 0), (2, 1, 0), (3, 0, -1), (4, 0, 1)]

class AreaPart:
    def __init__(self, kind, length):
        self.kind = kind
        self.length = length
    def __repr__(self):
        return f"({kind2char[self.kind]}, {self.length})"
    
    def __str__(self):
        return self.__repr__()

area = {}

oxygen_source = None
new_computer = None
def rek(pos, length, computer):
    global new_computer, oxygen_source
    if pos in area and area[pos].length > length:
        return
    if area[pos].kind == OXYGEN_SOURCE:
        oxygen_source = pos
        new_computer = copy.deepcopy(computer)
    pos_y, pos_x = pos
    for movement_code, delta_y, delta_x in movements:
        new_pos = pos_y + delta_y, pos_x + delta_x
        if new_pos in area:
            area_part = area[new_pos]
            if area_part.kind == WALL:
                continue
            if area_part.length >= length:
                continue
        else:
            computer_copy = copy.deepcopy(computer)
            output = computer_copy.run(movement_code)
            area[new_pos] = AreaPart(kind=output, length=length+1)
            if output == WALL:
                continue
            rek(new_pos, length+1, computer_copy)

field = {}
with open(sys.argv[1]) as f:
    for i, val in enumerate(map(int, f.read().strip().split(","))):
        field[i] = val

computer = Intcode(field)
init_pos = 0,0
area[init_pos] = AreaPart(kind=SPACE, length=0)
rek(init_pos, 0, computer)

min_x = min_y = INF
max_x = max_y = -INF
for pos in area:
    y, x = pos
    min_x = min(min_x, x)
    max_x = max(max_x, x)
    min_y = min(min_y, y)
    max_y = max(max_y, y)

rows = []
for y in range(min_y, max_y+1):
    row = []
    for x in range(min_x, max_x+1):
        if (y,x) in area:
            symbol = kind2char[area[y,x].kind]
        else:
            symbol = '?'
        row.append(symbol)
    rows.append("".join(row))
print("\n".join(rows))

area = {}
print("Oxygen source found at:", oxygen_source)
area[oxygen_source] = AreaPart(kind=OXYGEN_SOURCE, length=0)
rek(oxygen_source, 0, new_computer)

max_length = 0
for pos in area:
    if area[pos].kind == SPACE:
        max_length = max(max_length, area[pos].length)
print(max_length)