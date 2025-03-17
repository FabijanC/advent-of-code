import sys
import time
from util import Asteroid, DirectedLine
t1 = time.time()

asteroids = []
with open(sys.argv[1]) as f:
    for y, line in enumerate(f.readlines()):
        for x, el in enumerate(line):
            if el == '#':
                asteroids.append(Asteroid(x, y))        

sol = None
maxi = 0
for a1 in asteroids:
    cnt = 0
    for a2 in asteroids:
        if a1 is a2:
            continue
        line = DirectedLine(a1, a2)
        for other in asteroids:
            if other is a1 or other is a2:
                continue
            
            if other in line:
                break
        
        else:
            cnt += 1
    
    if cnt > maxi:
        sol = a1
        maxi = cnt

print(sol, maxi)
print("time:", time.time() - t1)