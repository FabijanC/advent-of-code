import sys
from sortedcontainers import SortedSet
import time
from graph_utils import get_neighbors
t1 = time.time()

class Config:
    def __init__(self, sym, collected_keys):
        self.sym = sym
        self.collected_keys = collected_keys
        self._hash = None
    
    def __eq__(self, other):
        return self.sym == other.sym and self.collected_keys == other.collected_keys

    def __hash__(self):
        if self._hash is None:
            self._hash = hash((self.sym, self.collected_keys))
        return self._hash

def heur(config):
    # are all doors necessarily unlocked?
    # perhaps find a minimum distance between two keys and multiply it with the number of keys (-1?)
    # return (TOTAL_KEYS - len(config.collected_keys))
    return 0
    key = 1
    cnt = 0
    for _ in range(TOTAL_KEYS):
        cnt += not (key & config.collected_keys)
        key <<= 1
    return cnt
    max_dist = 0
    for key in keys: # TODO OLD IMPLEMENTATION
        if key not in config.collected_keys:
            key_pos = keys[key]
            curr_dist = abs(key_pos[0] - config.pos[0]) + abs(key_pos[1] - config.pos[1])
            if curr_dist > max_dist:
                max_dist
    return max_dist

START = '@'
INF = int(1e9)

area = []
doors = {}
keys = {}
with open(sys.argv[1]) as f:
    for i, line in enumerate(f.readlines()):
        for j, el in enumerate(line):
            if el == START:
                start_pos = i, j
            elif el.islower():
                keys[ord(el)] = i, j
            elif el.isupper():
                doors[ord(el)] = i, j
        area.append(list(line.strip()))

TOTAL_KEYS = len(keys)
ALL_KEYS = (1 << TOTAL_KEYS) - 1
# area[start_pos[0]][start_pos[1]] = OPEN

start_config = Config(sym=ord(START), collected_keys=0)
gScore = {}
gScore[start_config] = 0

openSet = SortedSet(key=lambda pair: -pair[1])
openSet.add((start_config, 0))

nodes = {}
# make_graph(start, area, nodes)
nodes[ord(START)] = get_neighbors(start_pos, area)
for key in keys:
    nodes[key] = get_neighbors(keys[key], area)
for door in doors:
    nodes[door] = get_neighbors(doors[door], area)

while openSet:
    current, current_fScore = openSet.pop()
    if current.collected_keys == ALL_KEYS:
        print(current_fScore)
        break

    neighbors = nodes[current.sym]
    for neighbor_sym in neighbors:
        if neighbor_sym <= 90:# neighbor_sym.isupper():
            key = 1 << (neighbor_sym - 65)
            if key & current.collected_keys:
                pass
            else:
                continue
        
        next_collected_keys = current.collected_keys
        if neighbor_sym >= 97:# neighbor_sym.islower():
            next_collected_keys |= 1 << (neighbor_sym - 97)
        neighbor = Config(sym=neighbor_sym, collected_keys=next_collected_keys)

        tentative_gScore = gScore[current] + neighbors[neighbor_sym]
        if tentative_gScore < gScore.get(neighbor, INF):
            gScore[neighbor] = tentative_gScore
            #fScore = gScore[neighbor] + heur(neighbor)
            neighbor_pair = (neighbor, tentative_gScore)#fScore)
            if neighbor_pair not in openSet:
                openSet.add(neighbor_pair)

print("time:", time.time()-t1)