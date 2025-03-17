import sys
from sortedcontainers import SortedSet
import time
from graph_utils import make_graph
t1 = time.time()

class Config:
    def __init__(self, pos, collected_keys):
        self.pos = pos
        self.collected_keys = collected_keys
        self._hash = None
    
    def __eq__(self, other):
        return self.pos == other.pos and self.collected_keys == other.collected_keys

    def __hash__(self):
        if self._hash is None:
            self._hash = hash((self.pos, self.collected_keys))
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
    for key in keys:
        if key not in config.collected_keys:
            key_pos = keys[key]
            curr_dist = abs(key_pos[0] - config.pos[0]) + abs(key_pos[1] - config.pos[1])
            if curr_dist > max_dist:
                max_dist
    return max_dist

OPEN = '.'
START = '@'
WALL = '#'
INF = int(1e9)

area = []
doors = {}
keys = {}
with open(sys.argv[1]) as f:
    for i, line in enumerate(f.readlines()):
        for j, el in enumerate(line):
            if el == START:
                start = i, j
            elif el.islower():
                keys[el] = i, j
            elif el.isupper():
                doors[el] = i, j
        area.append(list(line.strip()))

TOTAL_KEYS = len(keys)
ALL_KEYS = (1 << TOTAL_KEYS) - 1
area[start[0]][start[1]] = OPEN

start_config = Config(pos=start, collected_keys=0)
gScore = {}
gScore[start_config] = 0

openSet = SortedSet(key=lambda pair: -pair[1])
openSet.add((start_config, heur(start_config)))

nodes = {}
make_graph(start, area, nodes)

while openSet:
    current, current_fScore = openSet.pop()
    if current.collected_keys == ALL_KEYS:
        print(current_fScore)
        break

    neighbors = nodes[current.pos]
    for neighbor_pos in neighbors:
        kind = area[neighbor_pos[0]][neighbor_pos[1]]
        if kind.isupper():
            key = 1 << (ord(kind) - ord('A'))
            if key & current.collected_keys:
                pass
            else:
                continue
        
        next_collected_keys = current.collected_keys
        if kind.islower():
            next_collected_keys |= 1 << (ord(kind) - ord('a')) # replace with a constant
        neighbor = Config(pos=neighbor_pos, collected_keys=next_collected_keys)

        tentative_gScore = gScore[current] + neighbors[neighbor_pos]
        if tentative_gScore < gScore.get(neighbor, INF):
            gScore[neighbor] = tentative_gScore
            fScore = gScore[neighbor] + heur(neighbor)
            neighbor_pair = (neighbor, fScore)
            if neighbor_pair not in openSet:
                openSet.add(neighbor_pair)

print("time:", time.time()-t1)