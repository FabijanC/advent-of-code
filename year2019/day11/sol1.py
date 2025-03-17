import sys
from robot import Robot

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

with open(sys.argv[1]) as f:
    field = {}
    for i, val in enumerate(map(int, f.read().strip().split(","))):
        field[i] = val

roby = Robot()
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
        val = roby.get_current_color()
        write(i+1, modes[-1], val)
        i += 2
    elif command == PUT:
        val = read(i+1, modes[-1])
        roby.progress(val)
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

print(roby.get_num_painted())
print(roby.show_painting())