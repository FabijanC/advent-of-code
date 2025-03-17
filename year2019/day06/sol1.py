import sys

parent = {}
children = {}

for line in sys.stdin:
    left, right = line.strip().split(")")
    if left not in children:
        children[left] = []
    parent[right] = left
    children[left].append(right)

potential_root = next(iter(parent.keys()))
while potential_root in parent:
    potential_root = parent[potential_root]

root = potential_root

sol = 0
stack = [(root, 0)]
while stack:
    planet, orbits = stack.pop()
    sol += orbits
    if planet not in children:
        continue
    for child in children[planet]:
        stack.append((child, orbits+1))

print(sol)