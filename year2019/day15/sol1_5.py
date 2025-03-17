from intcode import Intcode
import copy
import sys

INF = int(1e9)

WALL = 0
SPACE = 1
OXYGEN_SOURCE = 2
kind2char = {WALL: '#', SPACE: ' ', OXYGEN_SOURCE: 'O'}
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

def rek(pos, length, computer):
    if pos in area and area[pos].length > length:
        return
    # area[pos] = AreaPart(length=length, kind=SPACE)
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

for pos in area:
    area_part = area[pos]
    if area_part.kind == OXYGEN_SOURCE:
        print(pos, area_part.length)