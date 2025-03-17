import sys
from board import Board
import copy
import pickle
import numpy as np

I = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,2,0,0,2,0,2,2,0,2,0,2,2,2,2,2,2,0,0,2,0,2,2,2,2,0,2,0,0,0,2,0,0,2,0,0,0,0,0,0,0,2,0,0,1,1,0,0,2,0,0,2,2,0,2,0,0,0,0,2,2,2,0,0,0,0,0,0,2,2,2,0,0,2,0,0,2,2,0,2,2,0,0,0,0,2,2,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,0,2,2,0,0,2,0,0,2,0,0,0,0,2,0,0,2,2,2,0,0,2,2,0,2,2,2,2,0,1,1,0,2,0,0,2,2,2,2,2,0,0,2,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,2,0,2,0,0,2,0,0,0,0,0,0,0,1,1,0,2,2,0,2,2,0,2,2,0,0,2,2,0,0,0,2,0,0,2,0,0,0,2,2,2,2,2,2,0,2,0,0,0,0,0,2,0,2,0,2,2,0,0,1,1,0,2,0,2,0,2,0,2,0,0,2,0,0,0,2,2,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,0,2,0,0,0,2,0,2,2,0,2,2,0,1,1,0,2,0,2,0,0,2,0,0,2,0,0,2,2,0,0,2,2,2,0,0,2,0,0,2,2,0,0,2,0,2,0,0,0,0,0,2,2,2,0,0,2,2,0,1,1,0,2,0,0,0,2,2,2,0,2,0,0,2,0,0,0,0,2,2,2,0,0,2,0,2,0,2,2,2,2,0,0,2,0,0,0,0,2,0,0,2,2,0,0,1,1,0,2,0,0,0,2,2,2,2,0,2,2,0,0,2,0,0,0,0,0,2,2,0,2,2,2,0,2,0,0,2,2,2,2,0,2,0,2,0,0,0,0,0,0,1,1,0,2,0,0,0,2,2,2,0,2,2,0,0,0,2,0,2,2,0,2,0,0,0,0,0,2,2,0,2,2,0,2,0,2,0,0,0,2,2,0,0,0,0,0,1,1,0,2,0,0,0,2,2,2,2,0,0,0,0,2,0,0,2,0,2,0,0,0,2,0,2,2,0,2,0,2,0,0,0,2,0,0,2,0,2,0,2,0,2,0,1,1,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,2,2,0,0,0,2,0,2,0,2,2,2,2,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,1,1,0,0,0,0,2,0,2,2,0,0,0,0,0,2,0,0,0,2,2,0,0,2,2,2,0,0,2,2,0,2,0,0,0,0,0,0,0,0,0,2,0,2,0,0,1,1,0,0,0,2,0,0,2,0,0,0,2,2,0,2,2,2,0,2,2,2,0,0,0,2,0,2,2,0,0,2,2,0,2,2,0,2,2,2,2,0,2,2,2,0,1,1,0,0,0,2,0,0,2,0,2,0,2,2,2,0,0,0,0,0,2,0,0,2,2,2,0,2,2,0,0,2,2,0,0,2,0,2,0,2,0,2,2,0,0,0,1,1,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,2,2,2,0,0,0,0,2,0,0,2,0,0,2,0,2,0,0,2,2,0,0,2,0,0,0,0,1,1,0,2,2,2,2,2,2,2,0,2,0,0,0,0,2,0,0,2,0,0,0,0,2,2,2,0,2,0,2,0,0,2,0,0,0,0,2,2,2,2,2,2,0,0,1,1,0,2,0,0,2,0,0,0,2,0,0,0,2,2,2,0,0,2,0,0,0,2,0,2,2,2,0,0,0,2,2,0,0,0,2,2,0,0,2,2,2,0,2,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
I = np.array(I)
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
    #return field.get([(i,0), i, rel_base+field[i]][int(mode)],0)
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
        exit()
    elif mode == "2":
        field[rel_base + field[i]] = val

field = {}
with open(sys.argv[1]) as f:
    for i, val in enumerate(map(int, f.read().strip().split(","))):
        field[i] = val
field[0] = 2 # insert quarters
out_arr = [] # refreshes after three values
board = Board()
scores = []
storage = [""]*3

rel_base = 0
i = 0
while True:
    curr = str(field[i])
    curr = "0"*(5 - len(curr)) + curr
    modes, command = curr[:3], curr[3:]
    
    if command == HALT:
        print("HALT?", i)
        selected_storage = int(input())
        field, out_arr, board, scores, rel_base, i = pickle.loads(storage[selected_storage])
        print("UNPACKED", i, field[i])
    elif command == ADD:
        left = read(i+1, modes[-1]) 
        right = read(i+2, modes[-2])
        val = left + right
        # if val == 63: print (f"EXTRA:{modes} {field[i+1]} {field[i+2]}")
        # if board.switched: print(f"ADD: {val}={left}+{right}")
        write(i+3, modes[-3], val)
        i += 4
    elif command == MUL:
        left = read(i+1, modes[-1]) 
        right = read(i+2, modes[-2])
        val = left * right
        # if board.switched: print(f"MUL: {val}={left}*{right}")
        write(i+3, modes[-3], val)
        i += 4
    elif command == GET:
        # if board.switched:
        #     print(board.display())
        val = board.get_input()
        write(i+1, modes[-1], val)
        i += 2
    elif command == PUT:
        out_val = read(i+1, modes[-1])
        out_arr.append(out_val)
        if len(out_arr) == 3:
            pos = (out_arr[0], out_arr[1])
            if pos == (-1, 0):
                if not board.switched:
                    board.switch_to_matrix()
                    m = np.array(board.matrix)
                    m=m.reshape(len(I))
                    suma = np.sum(m == I)
                    # print(suma, len(I))
                    # exit()
                scores.append(out_arr[2])
                if out_arr[2] != 0:
                    storage[0:-1] = storage[1:]
                    storage[-1] = pickle.dumps((field, [], board, scores, rel_base, i+2))
                    print("COPIED at", i+2, field[i+2])
                s = scores[-1] - scores[-2] if len(scores) > 1 else None
                print(f"SCORE={out_arr[2]} by {modes}{command} from {i}, 0->{field[0]}")#", broken={board.last_broken}, points={s}")
            else:
                board.put(pos, out_arr[2])
            out_arr = []
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

print(scores)