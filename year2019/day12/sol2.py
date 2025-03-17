import sys
import re
import copy

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
    
    def __my_hash__(self, i):
        return hash((self.pos[i], self.vel[i]))

    def __hash__(self):
        return hash((tuple(self.pos), tuple(self.vel)))

def my_hash(planets, i):
    return hash(tuple(map(lambda p: p.__my_hash__(i), planets)))

LINE_RE = r"^<x=(.*), y=(.*), z=(.*)>$"

planets = []
with open(sys.argv[1]) as f:
    for line in f.readlines():
        found = re.findall(LINE_RE, line)[0]
        planet = Planet(list(map(int, found)))
        planets.append(planet)

planets = tuple(planets)
N_COORD = 3
N_PLANETS = len(planets)

for hash_coord in range(N_COORD):
    n_steps = 0
    hashes = dict()
    curr_hash = my_hash(planets, hash_coord)
    while curr_hash not in hashes:
        hashes[curr_hash] = copy.deepcopy(planets)
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
        
        curr_hash = my_hash(planets, hash_coord)
        n_steps += 1

    print(n_steps)
    