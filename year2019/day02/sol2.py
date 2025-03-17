ADD = 1
MUL = 2
HALT = 99

reserve_field = list(map(int, input().split(",")))

for x in range(0, 99+1):
    for y in range(0, 99+1):
        field = reserve_field.copy()
        field[1] = x
        field[2] = y

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
        
        if field[0] == 19690720:
            print(x, y)
            exit()