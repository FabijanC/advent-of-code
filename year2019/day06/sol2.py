import sys

parent = {}
for line in sys.stdin:
    left, right = line.strip().split(")")
    parent[right] = left

planet = "YOU"
you_trace = [planet]
planets_on_you_trace = set()
planets_on_you_trace.add(planet)
while planet in parent:
    planet = parent[planet]
    you_trace.append(planet)
    planets_on_you_trace.add(planet)

planet = "SAN"
san_cnt = -1
while planet in parent:
    planet = parent[planet]
    if planet in planets_on_you_trace:
        print(san_cnt + you_trace.index(planet))
        break
    san_cnt += 1