from collections import defaultdict
import sys

START = '@'
WALL = '#'
OPEN = '.'
DELTAS = [(1,0), (-1,0), (0,1), (0,-1)]

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

predecessors = defaultdict(list)
stack = [(start, 0, None)]
visited = set()
while stack:
    pos, dist, prev = stack.pop()
    i, j = pos
    val = area[i][j]
    if val == WALL:
        continue
    if pos in visited:
        continue
    visited.add(pos)

    if val.isalpha() or val == START:
        predecessors[val].append(prev)#((dist, prev))
        prev = val
    for di, dj in DELTAS:
        new_node = (i+di, j+dj), dist+1, prev
        stack.append(new_node)

for sym in sym2pos:
    if sym.isupper():
        predecessors[sym].append(sym.lower())

def toposort(node, predecessors, L, seen):#, total_cost):
    # for cost, predecessor in predecessors[node]:
    for predecessor in predecessors[node]:
        if predecessor not in seen:
            toposort(predecessor, predecessors, L, seen)#, total_cost + cost)
    L.append(node)#((total_cost, node))
    seen.add(node)

order = []
seen = set()
for sym in sym2pos:
    if sym.islower() and sym not in seen:
        toposort(sym, predecessors, order, seen)
print(order)