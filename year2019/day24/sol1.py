import sys

with open(sys.argv[1]) as f:
    field = f.read().strip().split("\n")

HEIGHT = len(field)
WIDTH = len(field[0])

BUG = '#'
EMPTY = '.'

sym2num = {
    EMPTY: 0,
    BUG: 1
}

def score(field):
    p = 1
    h = 0
    for i in range(len(field)):
        for j in range(len(field[0])):
            h = h + p*sym2num[field[i][j]]
            p <<= 1
    return h

DELTAS = [(1,0), (-1,0), (0,1), (0,-1)]
# print("\n".join(map(lambda line: "".join(line), field)) + "\n")
curr_score = score(field)
seen = set()
while curr_score not in seen:
    seen.add(curr_score)
    new_field = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for i in range(HEIGHT):
        for j in range(WIDTH):
            curr_kind = field[i][j]
            bug_cnt = 0
            for di, dj in DELTAS:
                ni, nj = i + di, j + dj
                if ni >= 0 and ni < HEIGHT and nj >= 0 and nj < WIDTH:
                    bug_cnt += field[ni][nj] == BUG
            if curr_kind == BUG and bug_cnt != 1:
                new_field[i][j] = EMPTY
            elif curr_kind == EMPTY and (bug_cnt == 1 or bug_cnt == 2):
                new_field[i][j] = BUG
            else:
                new_field[i][j] = field[i][j]
    field = new_field
    curr_score = score(field)
    # print("\n".join(map(lambda line: "".join(line), field)) + "\n")
            

print(score(field))

