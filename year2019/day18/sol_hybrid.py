import sys
from sortedcontainers import SortedSet
from copy import deepcopy
import time
t1 = time.clock()

class Config:
    def __init__(self, pos, collected_keys):
        self.pos = pos
        self.collected_keys = collected_keys
    
    def __eq__(self, other):
        return self.pos == other.pos and self.collected_keys == other.collected_keys

    def __hash__(self):
        return hash((self.pos, self.collected_keys))

def heur(config):
    # min_dist = 0
    # for door in config.unvisited_doors:
        # if door.lower() in config.collected_keys:
            # door_pos = doors[door]
            # curr_dist = abs(config.pos[0] - door_pos[0]) + abs(config.pos[1] - door_pos[1])
            # if curr_dist < min_dist:
                # min_dist = curr_dist
    # return min_dist
    # are all doors necessarily unlocked?
    # perhaps find a minimum distance between two keys and multiply it with the number of keys (-1?)
    return min_key[config.pos[0]][config.pos[1]]
    return 0
    return (TOTAL_KEYS - len(config.collected_keys))
    
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
door2pos = {}
pos2door = {}
key2pos = {}
pos2key = {}
MAX_PATH = 0
with open(sys.argv[1]) as f:
    for i, line in enumerate(f.readlines()):
        for j, el in enumerate(line):
            if el == START:
                start = i, j
            elif el.islower():
                key2pos[el] = i, j
                pos2key[i,j]=el
            elif el.isupper():
                door2pos[el] = i, j
                pos2door[i,j] = el
            if el != WALL:
                MAX_PATH += 2
        area.append(list(line.strip()))

assert len(door2pos) == len(pos2door)
assert len(key2pos) == len(pos2key)
HEIGHT = len(area)
WIDTH = len(area[0])
TOTAL_KEYS = len(key2pos)
TOTAL_DOORS = len(door2pos)
area[start[0]][start[1]] = OPEN

min_key = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)] #TODO None -> 0
for i in range(HEIGHT):
    for j in range(WIDTH):
        if area[i][j] != WALL:
            min_dist = INF
            for key in key2pos:
                key_pos = key2pos[key]
                curr_dist = abs(key_pos[0] - i) + abs(key_pos[1] - j)
                if curr_dist < min_dist:
                    min_dist = curr_dist
            min_key[i][j] = min_dist

start_config = Config(pos=start, collected_keys=frozenset())
gScore = {}
gScore[start_config] = 0

openSet = SortedSet(key=lambda pair: -pair[1])
openSet.add((start_config, heur(start_config)))

deltas = [(-1,0), (1,0), (0,-1), (0,1)]
lateral = {
    (-1,0): [(0,1), (0,-1)],
    (1,0): [(0,1), (0,-1)],
    (0,-1): [(1,0), (-1,0)],
    (0,1): [(1,0), (-1,0)]
}

while openSet:
    current, current_fScore = openSet.pop()
    if len(current.collected_keys) == TOTAL_KEYS:
        print(current_fScore)
        break
    neighbors = nodes[current.pos]
    for neighbor in neighbors:
    # for delta_i, delta_j in deltas:
        # neighbor_i, neighbor_j = current.pos
        # steps_taken = 0
        # tentative_collected_keys = set(current.collected_keys)
        # on_spot_for_branching = False
        # while True:
        #     neighbor_i, neighbor_j = neighbor_i + delta_i, neighbor_j + delta_j
        #     if neighbor_i < 0 or neighbor_i >= HEIGHT:
        #         break

        #     if neighbor_j < 0 or neighbor_j >= WIDTH:
        #         break
            
        #     kind = area[neighbor_i][neighbor_j]
        #     if kind == WALL or kind.isupper() and kind.lower() not in current.collected_keys:
        #         break

        #     steps_taken += 1

        #     # check if new key
        #     if kind.islower() and kind not in tentative_collected_keys:
        #         tentative_collected_keys.add(kind)
        #         on_spot_for_branching = True
        #         break
            
        #     lateral_wall, lateral_open = [], []
        #     for lateral_i, lateral_j in lateral[delta_i, delta_j]:
        #         neighbor_lateral_i, neighbor_lateral_j = neighbor_i + lateral_i, neighbor_j + lateral_j
        #         lateral_kind = area[neighbor_lateral_i][neighbor_lateral_j]
        #         if lateral_kind == WALL:
        #             lateral_wall.append((neighbor_lateral_i, neighbor_lateral_j))
        #         elif lateral_kind == OPEN:
        #             lateral_open.append((neighbor_lateral_i, neighbor_lateral_j))

        #     if len(lateral_wall) < 2: # crossroad
        #         on_spot_for_branching = True
        #         break
        
        # if not steps_taken:
        #     continue

        # if not on_spot_for_branching: # went by one too far, subtract
        #     neighbor_i, neighbor_j = neighbor_i - delta_i, neighbor_j - delta_j

        next_collected_keys = current.collected_keys
        if current.pos in pos2key:
            next_collected_keys =

        next_collected_keys = frozenset(tentative_collected_keys)
        neighbor = Config(pos=(neighbor_i, neighbor_j), collected_keys=next_collected_keys)

        tentative_gScore = gScore[current] + steps_taken
        if tentative_gScore < gScore.get(neighbor, INF):
            gScore[neighbor] = tentative_gScore
            fScore = tentative_gScore + heur(neighbor)
            neighbor_pair = (neighbor, fScore)
            if neighbor_pair not in openSet and tentative_gScore < MAX_PATH:
                openSet.add(neighbor_pair)

print("time:", time.clock()-t1)