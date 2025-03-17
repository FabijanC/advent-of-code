from collections import defaultdict
from collections import deque
import sys

START = '@'
WALL = '#'
OPEN = '.'
DELTAS = ((1,0), (-1,0), (0,1), (0,-1))
INF = int(1e9)

with open(sys.argv[1]) as f:
    area = f.read().strip().split("\n")

sym2pos = {}
for i, row in enumerate(area):
    for j, el in enumerate(row):
        if el == START:
            start = i, j
            sym2pos[el] = i,j
        elif el.isalpha():
            sym2pos[el] = i,j

distmap = {}
predecessors = defaultdict(list)
stack = deque([(start, 0, 0, None)])
visited = {}
while stack:
    pos, tot_dist, curr_dist, prev = stack.popleft()
    i, j = pos
    val = area[i][j]
    if val == WALL:
        continue
    # if val == prev:
    #     continue
    if visited.get(pos, INF) <= tot_dist:
        # this is true (only?) in cases like this: (i, j) -> (i, j+1) -> (i, j)
        continue
    visited[pos] = tot_dist

    if val.islower():
        predecessors[val].append(prev)
    elif val.isupper() or val == START:
        predecessors[val].append(prev)
        if prev is not None: distmap[val,prev] = distmap[prev,val] = curr_dist
        prev = val
        curr_dist = 0
    for di, dj in DELTAS:
        new_node = (i+di, j+dj), tot_dist+1, curr_dist+1, prev
        stack.append(new_node)

def get_distance(sym, goal):
    openset = deque()
    openset.append((sym2pos[sym], 0))
    visited = {}
    while openset:
        pos, dist = openset.popleft()
        i, j = pos
        val = area[i][j]
        if val == WALL:
            continue
        if visited.get(pos, INF) <= dist:
            continue
        visited[pos] = dist
        if val == goal:
            return dist
        for di, dj in DELTAS:
            new_node = (i+di, j+dj), dist+1
            openset.append(new_node)

for sym in sym2pos:
    if sym.isupper():
        key = sym.lower()
        dist = get_distance(sym, key) 
        predecessors[sym].append(key)
        # distmap[sym, key] = distmap[key, sym] = dist

symbols = list(sym2pos)
# for sym in symbols:
#     distmap[sym, sym] = 0
# for k in symbols:
#     for i in symbols:
#         for j in symbols:
#             tmpsum = distmap.get((i,k), INF) + distmap.get((k,j), INF)
#             if distmap.get((i,j), INF) > tmpsum:
#                 distmap[i,j] = tmpsum # symmetry?

# print(distmap)

for node in predecessors:
    print(node, predecessors[node])

def toposort(node, predecessors, L, seen):#, total_cost):
    for predecessor in sorted(predecessors[node], reverse=False):
        if predecessor not in seen:
            toposort(predecessor, predecessors, L, seen)#, total_cost + cost)
    L.append(node)
    seen.add(node)

order = []
seen = set()
for sym in sym2pos:
    if sym.islower() and sym not in seen:
        toposort(sym, predecessors, order, seen)
print(order)
total_dist = 0
for i in range(2, len(order)):
    d = get_distance(order[i-1], order[i])#distmap[order[i-1],order[i]]
    print(order[i-1], order[i],d)
    total_dist += d
print(total_dist)