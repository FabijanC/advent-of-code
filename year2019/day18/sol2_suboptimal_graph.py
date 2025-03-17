import sys
from sortedcontainers import SortedSet
import time
from graph_utils import make_graph
t1 = time.clock()

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
    # return 2*(TOTAL_KEYS - len(config.collected_keys))
    max_dist = [0,0,0,0]
    for key in keys:
        if key in config.collected_keys:
            continue
        key_pos = keys[key]
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
deltas = [(1,0), (-1,0), (0,1), (0,-1)]

area = []
doors = {}
keys = {}
start_pos = []
with open(sys.argv[1]) as f:
    for i, line in enumerate(f.readlines()):
        area.append(list(line.strip()))
        for j, el in enumerate(line):
            if el == START:
                start_pos.append((i, j))
                area[i][j] = OPEN
            elif el.islower():
                keys[el] = i, j
            elif el.isupper():
                doors[el] = i, j

HEIGHT = len(area)
WIDTH = len(area[0])
TOTAL_KEYS = len(keys)
TOTAL_DOORS = len(doors)

# quadrant = [[] for _ in range(4)]
key2quadrant = {}
center_i, center_j = start_pos[0][0]+1, start_pos[0][1]+1
for key in keys:
    key_i, key_j = keys[key]
    quadrant_index = 2*(key_i > center_i) + (key_j > center_j)
    key2quadrant[key] = quadrant_index
    # quadrant[quadrant_index].append(key)

nodes = {}
for pos in start_pos:
    make_graph(pos, area, nodes)

start_config = Config(pos=tuple(start_pos), collected_keys=frozenset())
gScore = {}
gScore[start_config] = 0

fScore = {}
fScore[start_config] = heur(start_config)

openSet = SortedSet(key=lambda pair: -pair[1])
openSet.add((start_config, fScore[start_config]))

while openSet:
    current, current_fScore = openSet.pop()
    if len(current.collected_keys) == TOTAL_KEYS:
        print(current_fScore)
        break

    for pos_i, pos in enumerate(current.pos):
        for delta_i, delta_j in deltas:
            neighbor_i, neighbor_j = pos
            steps_taken = 0
            tentative_collected_keys = set(current.collected_keys)
            on_spot_for_branching = False
            while True:
                neighbor_i, neighbor_j = neighbor_i + delta_i, neighbor_j + delta_j
                if neighbor_i < 0 or neighbor_i >= HEIGHT:
                    break

                if neighbor_j < 0 or neighbor_j >= WIDTH:
                    break
                
                kind = area[neighbor_i][neighbor_j]
                if kind == WALL or kind.isupper() and kind.lower() not in current.collected_keys:
                    break
                
                steps_taken += 1

                if kind.islower() and kind not in current.collected_keys:
                    tentative_collected_keys.add(kind)
                    on_spot_for_branching = True
                    break

                lateral_wall, lateral_open = [], []
                for lateral_i, lateral_j in lateral[delta_i, delta_j]:
                    neighbor_lateral_i, neighbor_lateral_j = neighbor_i + lateral_i, neighbor_j + lateral_j
                    lateral_kind = area[neighbor_lateral_i][neighbor_lateral_j]
                    if lateral_kind == WALL:
                        lateral_wall.append((neighbor_lateral_i, neighbor_lateral_j))
                    elif lateral_kind == OPEN:
                        lateral_open.append((neighbor_lateral_i, neighbor_lateral_j))

                if len(lateral_wall) < 2:
                    on_spot_for_branching = True
                    break

                assert len(lateral_wall) == 2
            
            if not steps_taken:
                continue

            if not on_spot_for_branching:
                neighbor_i, neighbor_j = neighbor_i - delta_i, neighbor_j - delta_j

            next_collected_keys = frozenset(tentative_collected_keys)
            next_pos = list(current.pos)
            next_pos[pos_i] = (neighbor_i, neighbor_j)
            next_pos = tuple(next_pos)
            neighbor = Config(pos=next_pos, collected_keys=next_collected_keys)

            tentative_gScore = gScore[current] + steps_taken
            if tentative_gScore < gScore.get(neighbor, INF):
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + heur(neighbor)
                neighbor_pair = (neighbor, fScore[neighbor])
                if neighbor_pair not in openSet:
                    openSet.add(neighbor_pair)

print("time:", time.clock()-t1)