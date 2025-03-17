import sys
from sortedcontainers import SortedSet
import time
from graph_utils import get_neighbors
t1 = time.clock()

class Config:
    def __init__(self, syms, collected_keys):
        self.syms = syms
        self.collected_keys = collected_keys
        self._hash = None
    
    def __eq__(self, other):
        return self.syms == other.syms and self.collected_keys == other.collected_keys

    def __hash__(self):
        if self._hash is None:
            self._hash = hash((self.syms, self.collected_keys))
        return self._hash

def heur(config):
    # are all doors necessarily unlocked?
    # perhaps find a minimum distance between two keys and multiply it with the number of keys (-1?)
    # return 2*(TOTAL_KEYS - len(config.collected_keys))
    return 0
    max_dist = [0,0,0,0]
    for key in key2pos:
        if key in config.collected_keys:
            continue
        key_pos = key2pos[key]
        q = key2quadrant[key]
        pos = config.pos[q]
        curr_dist = abs(key_pos[0] - pos[0]) + abs(key_pos[1] - pos[1])
        if curr_dist > max_dist[q]:
            max_dist[q] = curr_dist
    return sum(max_dist)

    # for pos_i, pos in enumerate(config.pos):
    #     max_dist = 0
    #     for key in quadrant[pos_i]:
    #         if key in config.collected_keys:
    #             continue
    #         key_pos = keys[key]
    #         curr_dist = abs(key_pos[0] - pos[0]) + abs(key_pos[1] - pos[1])
    #         if curr_dist > max_dist:
    #             max_dist = curr_dist
    #     tot_dist += max_dist
    # return tot_dist

OPEN = '.'
START = '@'
WALL = '#'
INF = int(1e9)

deltas = [(-1,0), (1,0), (0,-1), (0,1)]
lateral = {
    (-1,0): [(0,1), (0,-1)],
    (1,0): [(0,1), (0,-1)],
    (0,-1): [(1,0), (-1,0)],
    (0,1): [(1,0), (-1,0)]
}

area = []
door2pos = {}
pos2door = {}
key2pos = {}
pos2key = {}
start_pos = []
with open(sys.argv[1]) as f:
    for i, line in enumerate(f.readlines()):
        area.append(list(line.strip()))
        for j, el in enumerate(line):
            if el == START:
                start_pos.append((i, j))
                area[i][j] = OPEN
            elif el.islower():
                key2pos[el] = i, j
                pos2key[i,j] = el
            elif el.isupper():
                door2pos[el] = i, j
                pos2door[i,j] = el

TOTAL_KEYS = len(key2pos)
ALL_KEYS = (1 << TOTAL_KEYS) - 1

# quadrant = [[] for _ in range(4)]
key2quadrant = {}
center_i, center_j = start_pos[0][0]+1, start_pos[0][1]+1
for key in key2pos:
    key_i, key_j = key2pos[key]
    quadrant_index = 2*(key_i > center_i) + (key_j > center_j)
    key2quadrant[key] = quadrant_index
    # quadrant[quadrant_index].append(key)

nodes = {}
start_sym = []
for offset in range(4):
    start_sym.append(chr(ord(START)-offset))
for pos, sym in zip(start_pos, start_sym):
    nodes[sym] = get_neighbors(pos, area)
for key in key2pos:
    nodes[key] = get_neighbors(key2pos[key], area)
for door in door2pos:
    nodes[door] = get_neighbors(door2pos[door], area)

print("nodes:", len(nodes))
print("edges:", sum(map(len, nodes.values())))
print("edges sum:", sum(map(lambda node: sum(nodes[node].values()), nodes)))

# for node in nodes:
#     print(node, nodes[node])

start_config = Config(syms=tuple(start_sym), collected_keys=0)
gScore = {}
gScore[start_config] = 0

openSet = SortedSet(key=lambda pair: -pair[1])
openSet.add((start_config, 0))#heur(start_config)))

while openSet:
    current, current_fScore = openSet.pop()
    if current.collected_keys == ALL_KEYS:
        print(current_fScore)
        break

    for sym_i, sym in enumerate(current.syms):
        neighbors = nodes[sym]
        for neighbor_sym in neighbors:
            if neighbor_sym.isupper():
                key = 1 << (ord(neighbor_sym) - ord('A'))
                if key & current.collected_keys:
                    pass
                else:
                    continue
            
            next_collected_keys = current.collected_keys
            if neighbor_sym.islower():
                next_collected_keys |= 1 << (ord(neighbor_sym) - ord('a')) # replace with a constant
            
            next_sym = list(current.syms)
            next_sym[sym_i] = neighbor_sym
            next_sym = tuple(next_sym)
            neighbor = Config(syms=next_sym, collected_keys=next_collected_keys)

            tentative_gScore = gScore[current] + neighbors[neighbor_sym]
            if tentative_gScore < gScore.get(neighbor, INF):
                gScore[neighbor] = tentative_gScore
                # fScore = tentative_gScore + heur(neighbor)
                neighbor_pair = (neighbor, tentative_gScore)
                if neighbor_pair not in openSet:
                    openSet.add(neighbor_pair)

print("time:", time.clock()-t1)