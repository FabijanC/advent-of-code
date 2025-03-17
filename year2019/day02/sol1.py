ADD = 1
MUL = 2
HALT = 99

field = list(map(int, input().split(",")))
field[1] = 12
field[2] = 2

i = 0
while True:
    if field[i] == HALT:
        break
    elif field[i] == ADD:
        field[field[i+3]] = field[field[i+1]] + field[field[i+2]]
    elif field[i] == MUL:
        field[field[i+3]] = field[field[i+1]] * field[field[i+2]]
    else:
        print("Unknown opcode: ", field[i])
        exit()
    i += 4
print(field[0])