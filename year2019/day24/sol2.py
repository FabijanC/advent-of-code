import sys
import copy
import math

HEIGHT = 5
WIDTH = 5
CENTER = 2

BUG = 1
EMPTY = 0

def sym2num(sym):
    return BUG if sym == '#' else EMPTY

def default_field():
    return [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]

field0 = []
with open(sys.argv[1]) as f:
    for line in f.readlines():
        split_line = list(line.strip())
        field0.append(list(map(sym2num, split_line)))

N_MINUTES = int(sys.argv[2])
MAX_LVL = N_MINUTES // 2
MIN_LVL = -MAX_LVL
lvl2field = {}
for lvl in range(MIN_LVL-1, MAX_LVL+2):
    lvl2field[lvl] = default_field()
lvl2field[0] = field0

def single_cnt(field):
    cnt = 0
    assert field[CENTER][CENTER] == 0
    for i in range(HEIGHT):
        for j in range(WIDTH):
            cnt += field[i][j]
    return cnt

def cnt_left_right(lvl, i, j):
    if i == 2:
        if j == 0:
            return lvl2field[lvl-1][2][1] + lvl2field[lvl][i][1]
        elif j == 1:
            cnt = lvl2field[lvl][i][0]
            for inner_i in range(HEIGHT):
                cnt += lvl2field[lvl+1][inner_i][0]
            return cnt
        elif j == 3:
            cnt = lvl2field[lvl][i][4]
            for inner_i in range(HEIGHT):
                cnt += lvl2field[lvl+1][inner_i][4]
            return cnt
        elif j == WIDTH-1:
            return lvl2field[lvl][i][3] + lvl2field[lvl-1][2][3]
    else:
        if j == 0:
            return lvl2field[lvl-1][2][1] + lvl2field[lvl][i][j+1]
        elif j == WIDTH-1:
            return lvl2field[lvl][i][j-1] + lvl2field[lvl-1][2][3]
        else:
            return lvl2field[lvl][i][j-1] + lvl2field[lvl][i][j+1]

def cnt_infected_neighbors(lvl, i, j):
    cnt = cnt_left_right(lvl, i, j)
    if i == 0:
        cnt += lvl2field[lvl-1][i+1][2] + lvl2field[lvl][i+1][j] # above under
    elif i == 1:
        cnt += lvl2field[lvl][i-1][j] # above
        if j == 2: # under
            for inner_j in range(WIDTH):
                cnt += lvl2field[lvl+1][0][inner_j]
        else:
            cnt += lvl2field[lvl][i+1][j]
    elif i == 2:
        cnt += lvl2field[lvl][i-1][j] + lvl2field[lvl][i+1][j] # above under
    elif i == 3:
        cnt += lvl2field[lvl][i+1][j] # under
        if j == 2: # above
            for inner_j in range(WIDTH):
                cnt += lvl2field[lvl+1][4][inner_j]
        else:
            cnt += lvl2field[lvl][i-1][j]
    elif i == HEIGHT-1:
        cnt += lvl2field[lvl-1][i-1][2] + lvl2field[lvl][i-1][j]

    return cnt

# print("\n".join(map(lambda line: "".join(line), field)) + "\n")
for minute in range(N_MINUTES):
    new_lvl2field = copy.deepcopy(lvl2field)
    for lvl in range(MIN_LVL, MAX_LVL+1):
        # bugs_on_curr_lvl = single_cnt(lvl2field[lvl])
        # if bugs_on_curr_lvl == 0:
        #     continue
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if i == CENTER and j == CENTER:
                    continue
                curr_kind = lvl2field[lvl][i][j]
                bug_cnt = cnt_infected_neighbors(lvl, i, j)
                if curr_kind == BUG and bug_cnt != 1:
                    new_lvl2field[lvl][i][j] = EMPTY
                elif curr_kind == EMPTY and (bug_cnt == 1 or bug_cnt == 2):
                    new_lvl2field[lvl][i][j] = BUG
                # print(lvl, i, j, curr_kind, new_lvl2field[lvl][i][j])
                # else:
                #     new_field[i][j] = field[i][j]
    lvl2field = new_lvl2field
    # print("\n".join(map(lambda line: "".join(line), field)) + "\n")

final_cnt = 0
for field_i in lvl2field:
    field = lvl2field[field_i]
    print(field_i)
    for row in field:
        print(row)
    print()
    final_cnt += single_cnt(field)

print(final_cnt)