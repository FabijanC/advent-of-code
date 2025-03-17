import sys
import re

class Planet:
    def __init__(self, pos):
        self.pos = pos
        self.vel = [0,0,0]
    
    def __repr__(self):
        pos_str = ",".join(map(str, self.pos))
        vel_str = ",".join(map(str, self.vel))
        return f"pos=<{pos_str}>, vel=<{vel_str}>"

    def __str__(self):
        return self.__repr__()
    
    def __hash__(self):
        return hash((self.pos, self.vel))

LINE_RE = r"^<x=(.*), y=(.*), z=(.*)>$"

planets = []
with open(sys.argv[1]) as f:
    for line in f.readlines():
        found = re.findall(LINE_RE, line)[0]
        planet = Planet(list(map(int, found)))
        planets.append(planet)

N_COORD = 3
N_PLANETS = len(planets)

for step_i in range(int(sys.argv[2])):
    inc = [[0]*N_COORD for _ in range(N_PLANETS)]
    for i, planet in enumerate(planets):
        for j, other in enumerate(planets):
            if i == j: continue
            for c in range(N_COORD):
                if planet.pos[c] < other.pos[c]:
                    inc[i][c] += 1
                elif planet.pos[c] > other.pos[c]:
                    inc[i][c] -= 1
    
    for planet, inc_i in zip(planets, inc):
        for c in range(N_COORD):
            planet.vel[c] += inc_i[c]
    
    for planet in planets:
        for coord in range(N_COORD):
            planet.pos[coord] += planet.vel[coord]
    
    print(planets)

suma = 0
for planet in planets:
    pot = 0
    for coord in planet.pos:
        pot += abs(coord)
    kin = 0
    for vel_i in planet.vel:
        kin += abs(vel_i)
    suma += pot*kin

print(suma)
    