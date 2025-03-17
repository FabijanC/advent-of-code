import sys
import pickle

ADD = "01"
MUL = "02"
GET = "03"
PUT = "04"
JPT = "05"
JPF = "06"
LST = "07"
EQS = "08"
REL = "09"
HALT = "99"

def read(i, mode):
    if mode == "0":
        return field.get(field.get(i, 0), 0)
    elif mode == "1":
        return field.get(i, 0)
    elif mode == "2":
        return field.get(rel_base + field[i], 0)

def write(i, mode, val):
    if mode == "0":
        field[field[i]] = val
    elif mode == "1":
        print("ERROR")
    elif mode == "2":
        field[rel_base + field[i]] = val

def store():
    return pickle.dumps((field, i, rel_base))

def revert(storage):
    global field, i, rel_base
    field, i, rel_base = pickle.loads(storage)

class AreaPart:
    def __init__(self, kind, length, prev):
        self.kind = kind
        self.length = length
        self.prev = prev

field = {}
with open(sys.argv[1]) as f:
    for i, val in enumerate(map(int, f.read().strip().split(","))):
        field[i] = val

WALL = 0
SPACE = 1
FOUND = 2
movements = [(1, -1, 0), (2, 1, 0), (3, 0, -1), (4, 0, 1)]
area = {}
status = SPACE
pos_y, pos_x = 0, 0
desired_y, desired_x = 0, 0
curr_length = 0
FORWARD = 1
BACKWARD = -1
state = FORWARD

rel_base = 0
i = 0
while True:
    curr = str(field[i])
    curr = "0"*(5 - len(curr)) + curr
    modes, command = curr[:3], curr[3:]
    
    if command == HALT:
        break
    elif command == ADD:
        val = read(i+1, modes[-1]) + read(i+2, modes[-2])
        write(i+3, modes[-3], val)
        i += 4
    elif command == MUL:
        val = read(i+1, modes[-1]) * read(i+2, modes[-2])
        write(i+3, modes[-3], val)
        i += 4
    elif command == GET:
        pos = pos_y, pos_x
        if status == 0:
            area[pos] = AreaPart(kind=WALL, length=curr_length, prev=pos)
            continue
        
        if state == FORWARD:
            area[pos] = status, curr_length
            curr_length += 1
        else:
            curr_length -= 1
        for movement_code, delta_y, delta_x in movements:
            new_pos = pos_y + delta_y, pos_x + delta_x
            if new_pos not in area:
                break
            other_kind, other_length = area[new_pos]
            if other_kind != WALL and curr_length < other_length:
                break
        else:
            ... + ...
            continue

        write(i+1, modes[-1], movement_code)
        i += 2
    elif command == PUT:
        status = read(i+1, modes[-1])
        i += 2
    elif command == JPT:
        if read(i+1, modes[-1]):
            i = read(i+2, modes[-2])
        else:
            i += 3
    elif command == JPF:
        if not read(i+1, modes[-1]):
            i = read(i+2, modes[-2])
        else:
            i += 3
    elif command == LST:
        first = read(i+1, modes[-1])
        second = read(i+2, modes[-2])
        val = int(first < second)
        write(i+3, modes[-3], val)
        i += 4
    elif command == EQS:
        first = read(i+1, modes[-1])
        second = read(i+2, modes[-2])
        val = int(first == second)
        write(i+3, modes[-3], val)
        i += 4
    elif command == REL:
        delta = read(i+1, modes[-1])
        rel_base += delta
        i += 2
    else:
        print("Unknown opcode: ", command)
        exit()