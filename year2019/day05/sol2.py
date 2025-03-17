import sys

ADD = "01"
MUL = "02"
GET = "03"
PUT = "04"
JPT = "05"
JPF = "06"
LST = "07"
EQS = "08"
HALT = "99"

def read(i, mode):
    return field[i] if mode == "1" else field[field[i]]

field = list(map(int, input().split(",")))
i = 0
while True:
    curr = str(field[i])
    curr = "0"*(5 - len(curr)) + curr
    modes, command = curr[:3], curr[3:]
    
    if command == HALT:
        break
    elif command == ADD:
        field[field[i+3]] = read(i+1, modes[-1]) + read(i+2, modes[-2])
        i += 4
    elif command == MUL:
        field[field[i+3]] = read(i+1, modes[-1]) * read(i+2, modes[-2])
        i += 4
    elif command == GET:
        field[field[i+1]] = int(sys.argv[1])
        i += 2
    elif command == PUT:
        print(read(i+1, modes[2]))
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
        field[field[i+3]] = int(first < second)
        i += 4
    elif command == EQS:
        first = read(i+1, modes[-1])
        second = read(i+2, modes[-2])
        field[field[i+3]] = int(first == second)
        i += 4
    else:
        print("Unknown opcode: ", command)
        exit()