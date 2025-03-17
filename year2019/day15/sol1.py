import sys
import readchar

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
FOUND = '%'

key2num = {'w': 1, 's': 2, 'a': 3, 'd': 4}
key2delta = {'w': (-1,0), 's': (1,0), 'a': (0,-1), 'd': (0,1)}

HEIGHT = 60
WIDTH = 60
area = [[UNKNOWN for _ in range(WIDTH)] for _ in range(HEIGHT)]
length = {}
init_y, init_x = HEIGHT // 2, WIDTH // 2
pos_y, pos_x = init_y,init_x
curr_length = 0
length[pos_y, pos_x] = curr_length
desired_y, desired_x = pos_y, pos_x
status = 1

def display(matrix, position):
    print(position, curr_length)
    y, x = position
    matrix[y][x] = DROID
    output = []
    for row in matrix:
        output.append("".join(row))
    print("\n".join(output))
    matrix[y][x] = SPACE

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
        if status == 0:
            area[desired_y][desired_x] = WALL
        else:
            pos_y, pos_x = desired_y, desired_x
            area[pos_y][pos_x] = SPACE if status == 1 else FOUND
            if (pos_y, pos_x) not in length:
                length[pos_y, pos_x] = curr_length
            else:
                length[pos_y, pos_x] = min(length[pos_y, pos_x], curr_length)
            curr_length = length[pos_y, pos_x] + 1
            # area[desired_y][desired_x] = FOUND
            # print("FOUND", desired_y, desired_x, "in", curr_length) # 18, 46
        display(area, (pos_y, pos_x))
        
        key = None
        while key not in key2num:
            key = readchar.readkey()
        write(i+1, modes[-1], key2num[key])
        delta_y, delta_x = key2delta[key]
        desired_y, desired_x = pos_y + delta_y, pos_x + delta_x
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