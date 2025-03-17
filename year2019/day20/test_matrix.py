import time
import sys


N = int(sys.argv[1])
area = [[1 for _ in range(N)] for _ in range(N)]

t1 = time.clock()
suma = 0
for i in range(N):
    for j in range(N):
        suma += area[i][j]
#print(suma)
print(time.clock() - t1)