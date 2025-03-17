from sys import path
from os.path import dirname
path.append(dirname(path[0]))
from intcode import Intcode
import sys

SCAFFOLD = '#'

computer = Intcode(file_name=sys.argv[1])
computer.field[0] = 2

area = [[]]
while computer.state == Intcode.OK:
    output = computer.run()
    if output is None:
        break
    output = chr(output)
    if output == '\n':
        area.append([])
        print()
    else:
        area[-1].append(output)
        print(output, end="")

while len(area[-1]) != len(area[0]):
    area.pop()

class Direction:
    dirs = {}
    def __init__(self, name, forward, left, right):
        self.name = name
        self.forward = forward
        self.left = left
        self.right = right
        Direction.dirs[name] = self
    
    def apply(self, pos_i, pos_j):
        return pos_i + self.forward[0], pos_j + self.forward[1]
    
    def get_left(self):
        return Direction.dirs[self.left]
    
    def get_right(self):
        return Direction.dirs[self.right]

dirs = [
    Direction(name="UP", forward=(-1,0), left="LEFT", right="RIGHT"),
    Direction(name="DOWN", forward=(1, 0), left="RIGHT", right="LEFT"),
    Direction(name="LEFT", forward=(0,-1), left="DOWN", right="UP"),
    Direction(name="RIGHT", forward=(0,1), left="UP", right="DOWN")
]

found = False
for i, row in enumerate(area):
    for j, el in enumerate(row):
        if el == "^":
            found = True
            break
    if found:
        break

def legal(i, j):
    return i >= 0 and i < legal.height and j >= 0 and j < legal.width and area[i][j] == SCAFFOLD
legal.height = len(area)
legal.width = len(area[0])

curr_i, curr_j = i, j
area[curr_i][curr_j] = SCAFFOLD
curr_dir = dirs[0]
step_cnt = 0
commands = []
while True:
    new_i, new_j = curr_dir.apply(curr_i, curr_j)
    if legal(new_i, new_j):
        step_cnt += 1
        curr_i, curr_j = new_i, new_j
    else:
        if step_cnt: commands.append(str(step_cnt))
        step_cnt = 0

        old = curr_dir
        left = curr_dir.get_left()
        right = curr_dir.get_right()
        if legal(*left.apply(curr_i, curr_j)):
            commands.append("L")
            curr_dir = left
        elif legal(*right.apply(curr_i, curr_j)):
            commands.append("R")
            curr_dir = right
        else:
            break

# for row in area:
#     print("".join(row))
commands_str = ",".join(commands)

A = "L,4,L,4,L,10,R,4"
B = "R,4,L,4,L,4,R,8,R,10"
C = "R,4,L,10,R,10"
hardcoded_movement = "A,B,A,C,A,C,B,C,C,B"
movement = commands_str.replace(A, "A").replace(B, "B").replace(C, "C")
assert hardcoded_movement == movement
MAX_LOGIC_LEN = 20
assert len(movement) <= MAX_LOGIC_LEN
assert len(A) <= MAX_LOGIC_LEN
assert len(B) <= MAX_LOGIC_LEN
assert len(C) <= MAX_LOGIC_LEN

input_chars = map(ord, "\n".join([movement, A, B, C]) + "\nn\n")
computer.put(input_chars)
outputs = []
while True:
    output = computer.run()
    if output is not None:
        print(chr(output), end="")
        outputs.append(output)
    else:
        break

print(outputs[-1])