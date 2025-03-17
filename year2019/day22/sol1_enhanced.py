import sys

with open(sys.argv[1]) as f:
    lines = f.read().strip().split("\n")

REVERSE = 0
CUT = 1
INC = 2
shuffles = []
for line in lines:
    if line == "deal into new stack":
        shuffles.append((REVERSE,))
        continue

    technique, val = line.rsplit(" ", 1)
    val = int(val)
    if technique.startswith("cut"):
        shuffles.append((CUT, val))
    elif technique.startswith("deal with"):
        shuffles.append((INC, val))
    else:
        raise ValueError("Error in parsing line:", line)

sol = 2019
DECK_SIZE = 10007
for shuffle_i, shuffle in enumerate(shuffles):
    code = shuffle[0]
    if code == REVERSE:
        sol = DECK_SIZE - sol - 1
    elif code == CUT:
        sol = (sol - shuffle[1] + DECK_SIZE) % DECK_SIZE
    else:
        sol = (sol * shuffle[1]) % DECK_SIZE
print(sol)