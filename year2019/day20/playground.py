import sys
import heapq
import time

def pretty(area):
    for line in area:
        print("".join(map(lambda val: val[0] if len(val) == 2 else val, line)))
    print()

with open(sys.argv[1]) as f:
    area = f.read().strip("\n").split("\n")

height = len(area)
width = len(area[0])
# area_height = lines_height - 4
# area_width = lines_width - 4

# area = [[lines[i+2][j+2] if not lines[i+2][j+2].isalpha() else ' ' for j in range(area_width)] for i in range(area_height)]

# # top
# for j, val in enumerate(lines[0]):
#     if val.isalpha():
#         area[0][j-2] = lines[0][j] + lines[1][j]

# # bottom
# for j, val in enumerate(lines[-1]):
#     if val.isalpha():
#         area[-1][j-2] = lines[-2][j] + lines[-1][j]

# # left
# for i in range(lines_height):
#     val = lines[i][0]
#     if val.isalpha():
#         area[i-2][0] = lines[i][:2]

# # right
# for i in range(lines_height):
#     val = lines[i][-2]
#     if val.isalpha():
#         area[i-2][-1] = lines[i][-2:]

# #inside
# inner_start = 2
# BLOCK_CHARS = '#.'
# while lines[inner_start][inner_start] in BLOCK_CHARS:
#     inner_start += 1
# inner_end_i = lines_height - inner_start
# inner_end_j = lines_width - inner_start

# for j in range(inner_start, inner_end_j):
#     # inside top
#     if lines[inner_start][j].isalpha():
#         area[inner_start-3][j-2] = lines[inner_start][j] + lines[inner_start+1][j]
#     # inside bottom
#     if lines[inner_end_i-1][j].isalpha():
#         area[inner_end_i-2][j-2] = lines[inner_end_i-2][j] + lines[inner_end_i-1][j]

# for i in range(inner_start, inner_end_i):
#     # inside left
#     if lines[i][inner_start].isalpha():
#         area[i-2][inner_start-3] = lines[i][inner_start] + lines[i][inner_start+1]
#     # inside right
#     if lines[i][inner_end_j-1].isalpha():
#         area[i-2][inner_end_j-2] = lines[i][inner_end_j-2] + lines[i-2][inner_end_j-1]

# pretty(area)

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

def move(pos, d, area, stack):
    ni, nj = pos
    steps_taken = 0
    while True:
        forward = ni + d[0], nj + d[1]
        forward_el = area[forward[0]][forward[1]]
        left, right = LATERAL[ni,nj]
        left_pos = ni+left[0], nj+left[1]
        left_el = area[ni+left[0]][nj+left[1]]
        right_pos = ni+right[0], nj+right[1]
        right_el = area[ni+right[0]][nj+right[1]]

        if forward_el == WALL:
            if left_el == WALL and right_el == WALL:
                break
            elif left_el == WALL and right_el == OPEN:
                d = right
            elif left_el == OPEN and right_el == WALL:
                d = left
        elif forward_el.isalpha(): # ahead: open field but special
            new_pos, d = area.portals[forward]
            ni, nj = new_pos
        else: # ahead: plain open field
            if left_el == OPEN:
                # TODO
                ni, nj = forward
                break

        
        ni, nj = ni + d[0], nj + d[1]
        steps_taken += 1
    
    return (ni, nj), steps_taken

def dijkstra(start_pos, nodes):
    openset = [(0, start_pos)]
    node = nodes[start_pos]
    scores = {pos: INF for pos in node.neighbors}

    while openset:
        score, pos = heapq.heappop(openset)
        node = nodes[pos]
        for neighbor in node.neighbors:
            old_score = scores[neighbor]
            tentative_score = score + node.neighbors[neighbor]
            if tentative_score < old_score:
                scores[neighbor] = tentative_score
                heapq.heappush((scores[neighbor], neighbor)) # TODO
    
    return scores

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

    AA_pos = SYMBOL2POS["AA"]
    stack = [(AA_pos)]
    visited = set()
    while stack:
        i, j = pos = stack.pop()
        el = area[i][j]
        if el == WALL or el == OPEN:
            continue
        if pos in visited:
            continue
        visited.add(pos)

        neighbors = {}
        for d in DELTAS:
            ni, nj = i + d[0], j + d[1]
            new_el = area[ni][nj]

            

            if new_el.isalpha(): # if neighbor is portal
                node.symbol = new_el + area[ni+d[0]][nj+d[1]]
            if new_el == WALL:
                continue
            else: # else it's open; move as far as possible
                new_pos, steps_taken = move((i,j), d, area, visited)
                assert steps_taken
                neighbors[new_pos] = steps_taken
        nodes[i,j] = neighbors
    
if __name__ == "__main__":
    main(sys.argv[1])