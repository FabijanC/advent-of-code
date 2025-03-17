import sys
import heapq
import time

INF = int(1e9)

UP = (-1,0)
DOWN = (1,0)
LEFT = (0,-1)
RIGHT = (0,1)
DELTAS = [UP, DOWN, LEFT, RIGHT]
LATERAL = {
    UP: (LEFT, RIGHT),
    DOWN: (RIGHT, LEFT),
    LEFT: (DOWN, UP),
    RIGHT: (UP, DOWN)
}

WALL = '#'
OUT = ' '
OPEN = '.'
BLOCK_CHARS = WALL + OPEN

SYMBOL2POS = {}
PORTALS = [{}, {}]
INWARD = False
OUTWARD = True

MAX_DEPTH = 50
MAX_DIST = 10000

def add_if_possible(symbol, pos, wardness):
    if symbol.isalpha():
        if symbol in SYMBOL2POS:
            old_pos = SYMBOL2POS[symbol]
            PORTALS[not wardness][old_pos] = pos
            PORTALS[wardness][pos] = old_pos
        else:
            SYMBOL2POS[symbol] = pos

def search_row(area, i, start_j, end_j, shift_i, wardness):
    for j in range(start_j, end_j):
        add_if_possible(area[i][j] + area[i+1][j], (i+shift_i,j), wardness)

def search_col(area, start_i, end_i, j, shift_j, wardness):
    for i in range(start_i, end_i):
        add_if_possible(area[i][j] + area[i][j+1], (i,j+shift_j), wardness)

def find_inner_start(area):
    inner_start = 2
    while area[inner_start][inner_start] in BLOCK_CHARS:
        inner_start += 1
    return inner_start

def main(input_path):
    with open(input_path) as f:
        area = f.read().strip("\n").split("\n")

    height = len(area)
    width = len(area[0])
    nodes = []

    search_row(area, i=0, start_j=2, end_j=width-2, shift_i=+2, wardness=OUTWARD)
    search_row(area, i=height-2, start_j=2, end_j=width-2, shift_i=-1, wardness=OUTWARD)
    search_col(area, start_i=2, end_i=height-2, j=0, shift_j=+2, wardness=OUTWARD)
    search_col(area, start_i=2, end_i=height-2, j=width-2, shift_j=-1, wardness=OUTWARD)
    
    inner_start = find_inner_start(area)
    inner_end_i = height - inner_start
    inner_end_j = width - inner_start
    #print(inner_start, inner_end_i, inner_end_j)
    search_row(area, i=inner_start, start_j=inner_start, end_j=inner_end_j, shift_i=-1, wardness=INWARD)
    search_row(area, i=inner_end_i-2, start_j=inner_start, end_j=inner_end_j, shift_i=+2, wardness=INWARD)
    search_col(area, start_i=inner_start, end_i=inner_end_i, j=inner_start, shift_j=-1, wardness=INWARD)
    search_col(area, start_i=inner_start, end_i=inner_end_i, j=inner_end_j-2, shift_j=+2, wardness=INWARD)

    print(PORTALS, SYMBOL2POS)

    AA_pos = SYMBOL2POS["AA"] + (0,)
    openset = [(0, AA_pos)]
    been = {}

    while openset:
        dist, pos = openset.pop()
        # dist, pos = heapq.heappop(openset)
        i, j, z = pos
        if area[i][j] != OPEN:
            continue

        if z < 0 or z > MAX_DEPTH or dist > MAX_DIST:
            continue

        if been.get(pos, INF) < dist:
            continue
        been[pos] = dist
        
        if (i,j) in PORTALS[INWARD]:
            openset.append((dist+1, PORTALS[INWARD][i,j] + (z + 1,)))
            # heapq.heappush(openset, (dist+1, PORTALS[INWARD][i,j] + (z + 1,)))
        elif (i,j) in PORTALS[OUTWARD]:
            openset.append((dist+1, PORTALS[OUTWARD][i,j] + (z - 1,)))
            #heapq.heappush(openset, (dist+1, PORTALS[OUTWARD][i,j] + (z - 1,)))

        for di, dj in DELTAS:
            openset.append((dist+1, (i+di, j+dj, z)))
            #heapq.heappush(openset, (dist+1, (i+di, j+dj, z)))
    
    ZZ_pos = SYMBOL2POS["ZZ"] + (0,)
    print(been[ZZ_pos])
 
if __name__ == "__main__":
    t1 = time.clock()
    main(sys.argv[1])
    print(time.clock() - t1)