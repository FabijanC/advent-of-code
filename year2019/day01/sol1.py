import math
import sys

sol = 0
for line in sys.stdin:
    sol += int(line) // 3 - 2
print(sol)