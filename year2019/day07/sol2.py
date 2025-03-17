import sys
import itertools
import copy
from collections import deque

ADD = "01"
MUL = "02"
GET = "03"
PUT = "04"
JPT = "05"
JPF = "06"
LST = "07"
EQS = "08"
HALT = "99"

MIN_PHASE = 5
MAX_PHASE = 9
COMP_N = MAX_PHASE - MIN_PHASE + 1
INF = int(1e9)

def read(i, mode):
    return field[i] if mode == "1" else field[field[i]]

with open(sys.argv[1]) as f:
    line = f.read()
field_instance = list(map(int, line.strip().split(",")))
storage = [field_instance.copy() for _ in range(COMP_N)]

max_output = -INF
max_comb = None
for phases in itertools.permutations(range(MIN_PHASE, MAX_PHASE+1)):
    outputs = [deque() for _ in range(COMP_N)]
    outputs[-1].appendleft(0)
    comp_i = 0
    halt_cnt = 0
    GET_called = [False]*COMP_N
    field_arr = copy.deepcopy(storage)
    i_arr = [0]*COMP_N
    while halt_cnt < COMP_N:
        #import pdb; pdb.set_trace()
        field = field_arr[comp_i]
        i = i_arr[comp_i]
        while True:
            curr = str(field[i])
            curr = "0"*(5 - len(curr)) + curr
            modes, command = curr[:3], curr[3:]
            
            if command == HALT:
                halt_cnt += 1
                #print("halting", comp_i)
                break
            elif command == ADD:
                field[field[i+3]] = read(i+1, modes[-1]) + read(i+2, modes[-2])
                i += 4
            elif command == MUL:
                field[field[i+3]] = read(i+1, modes[-1]) * read(i+2, modes[-2])
                i += 4
            elif command == GET:
                if not GET_called[comp_i]:
                    gotten = phases[comp_i]
                    GET_called[comp_i] = True
                else:
                    input_list = outputs[(comp_i - 1 + COMP_N) % COMP_N]
                    if input_list:
                        gotten = input_list.pop()
                    else:
                        break
                field[field[i+1]] = gotten
                i += 2
            elif command == PUT:
                output = read(i+1, modes[2])
                outputs[comp_i].appendleft(output)
                #print(f"PUT of {comp_i}: {outputs[comp_i]}")
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
        
        i_arr[comp_i] = i
        comp_i = (comp_i + 1) % COMP_N
        
    last_output = outputs[COMP_N - 1].pop()
    if last_output > max_output:
        max_output = last_output
        max_comb = phases

print(max_comb, max_output)