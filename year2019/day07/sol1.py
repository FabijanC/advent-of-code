import itertools

ADD = "01"
MUL = "02"
GET = "03"
PUT = "04"
JPT = "05"
JPF = "06"
LST = "07"
EQS = "08"
HALT = "99"

MIN_PHASE = 0
MAX_PHASE = 4
COMP_N = 5
INF = int(1e9)

def read(i, mode):
    return field[i] if mode == "1" else field[field[i]]

storage = list(map(int, input().split(",")))

max_output = -INF
max_comb = None
for phases in itertools.permutations(range(MIN_PHASE, MAX_PHASE+1)):
    prev_output = 0
    for comp_i in range(COMP_N):
        field = storage.copy()
        GET_called = False
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
                if not GET_called:
                    gotten = phases[comp_i]
                    GET_called = True
                else:
                    gotten = prev_output
                field[field[i+1]] = gotten
                i += 2
            elif command == PUT:
                prev_output = read(i+1, modes[2])
                #print(prev_output)
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
    
    if prev_output > max_output:
        print("new max:", prev_output)
        max_output = prev_output
        max_comb = phases

print(max_comb, max_output)