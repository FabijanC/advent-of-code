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

field = {}
with open(sys.argv[1]) as f:
    for i, val in enumerate(map(int, f.read().strip().split(","))):
        field[i] = val

UNKNOWN = '.'
WALL = '#'
SPACE = ' '
DROID = 'D'

movement2delta = [None, (-1,0), (1,0), (0,-1), (0,1)]

rel_base = 0
i = 0

area = {}
pos_y, pos_x = 0,0
status = 1
length = 0
stack = [(pos_y, pos_x, length, pickle.dumps((field, i, rel_base)))]

def revert():
    global field, i, rel_base
    field, i, rel_base = pickle.loads(storage)

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
        pos_y, pos_x, length, storage = stack.pop()
        if status == 0:
            area[pos_y, pos_x] = (WALL, length)
            revert()
            continue
        elif status == 2:
            print(pos_y, pos_x, length)
            break

        for movement in range(1, 4+1):
            delta_y, delta_x = movement2delta[move_code]
            next_y, next_x = pos_y + delta_y, pos_x + delta_x
            if (next_y, next_x) in area:
                continue
            kind, other_length = area[next_y, next_x]
            if kind == WALL or other_length <= length:
                continue
        else:
            ... = revert()
        if length >= :
            revert()
            continue
        area[pos_y,pos_x] = (SPACE, length)
        
        write(i+1, modes[-1], movement)
        delta_y, delta_x = movement2delta[movement]
        pos_y, pos_x = pos_y + delta_y, pos_x + delta_x
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