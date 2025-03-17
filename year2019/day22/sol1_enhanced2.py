import sys

with open(sys.argv[1]) as f:
    lines = f.read().strip().split("\n")

QUERY = 2019
DECK_SIZE = 10007
N_STEPS = 101741582076661

expr = [1, 0]
for line in lines:
    t, v = line.rsplit(" ", 1)
    if line == "deal into new stack":
        expr[0] = (-expr[0]) % DECK_SIZE
        expr[1] = (-expr[1] - 1) % DECK_SIZE
    elif line.startswith("deal with"):
        expr[0] = (expr[0] * int(v)) % DECK_SIZE
        expr[1] = (expr[1] * int(v)) % DECK_SIZE
    else:
        expr[1] = (expr[1] - int(v)) % DECK_SIZE

print((expr[0] * QUERY + expr[1]) % DECK_SIZE)