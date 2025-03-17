import sys
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
PORTALS = {}

def add_if_possible(symbol, pos):
    if symbol.isalpha():
        if symbol in SYMBOL2POS:
            old_pos = SYMBOL2POS[symbol]
            PORTALS[old_pos] = pos
            PORTALS[pos] = old_pos
        else:
            SYMBOL2POS[symbol] = pos

def search_row(area, i, start_j, end_j, shift_i):
    for j in range(start_j, end_j):
        add_if_possible(area[i][j] + area[i+1][j], (i+shift_i,j))

def search_col(area, start_i, end_i, j, shift_j):
    for i in range(start_i, end_i):
        add_if_possible(area[i][j] + area[i][j+1], (i,j+shift_j))

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

    search_row(area, i=0, start_j=2, end_j=width-2, shift_i=+2)
    search_row(area, i=height-2, start_j=2, end_j=width-2, shift_i=-1)
    search_col(area, start_i=2, end_i=height-2, j=0, shift_j=+2)
    search_col(area, start_i=2, end_i=height-2, j=width-2, shift_j=-1)
    
    inner_start = find_inner_start(area)
    inner_end_i = height - inner_start
    inner_end_j = width - inner_start
    
    search_row(area, i=inner_start, start_j=inner_start, end_j=inner_end_j, shift_i=-1)
    search_row(area, i=inner_end_i-2, start_j=inner_start, end_j=inner_end_j, shift_i=+2)
    search_col(area, start_i=inner_start, end_i=inner_end_i, j=inner_start, shift_j=-1)
    search_col(area, start_i=inner_start, end_i=inner_end_i, j=inner_end_j-2, shift_j=+2)

    AA_pos = SYMBOL2POS["AA"]
    stack = [(0, AA_pos)]
    been = {}

    while stack:
        depth, pos = stack.pop()
        i, j = pos
        if area[i][j] != OPEN:
            continue

        if been.get(pos, INF) < depth:
            continue
        been[pos] = depth
        
        if pos in PORTALS:
            stack.append((depth+1, PORTALS[pos]))
        
        for di, dj in DELTAS:
            stack.append((depth+1, (i+di, j+dj)))
    
    ZZ_pos = SYMBOL2POS["ZZ"]
    print(been[ZZ_pos])
    
if __name__ == "__main__":
    main(sys.argv[1])