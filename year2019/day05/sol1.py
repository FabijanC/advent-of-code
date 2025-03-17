import sys

ADD = "01"
MUL = "02"
GET = "03"
PUT = "04"
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
    else:
        print("Unknown opcode: ", command)
        exit()