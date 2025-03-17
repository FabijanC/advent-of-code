import sys
from intcode import Intcode

field = {}
with open(sys.argv[2]) as f:
    for i, val in enumerate(map(int, f.read().strip().split(","))):
        field[i] = val

intcode = Intcode(field, print)
intcode.run(int(sys.argv[1]))