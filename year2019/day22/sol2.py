import sys

def mod_pow(b, e, p):
    if e == 1:
        return b % p
    a = mod_pow(b, e//2, p)
    ret = (a*a) % p
    if e % 2 == 1:
        ret = (ret*b) % p
    return ret

with open(sys.argv[1]) as f:
    lines = f.read().strip().split("\n")

QUERY = 2020
DECK_SIZE = 119315717514047
N_STEPS = 101741582076661

REVERSE = 0
CUT = 1
INC = 2
shuffles = []
expr = [1, 0]
for line in reversed(lines):
    t, v = line.rsplit(" ", 1)
    if line == "deal into new stack":
        expr[0] = (-expr[0]) % DECK_SIZE
        expr[1] = (-expr[1] - 1) % DECK_SIZE
    elif line.startswith("deal with"):
        val = int(v)
        mod_mul_inv = mod_pow(val, DECK_SIZE-2, DECK_SIZE)
        expr[0] = (expr[0] * mod_mul_inv) % DECK_SIZE
        expr[1] = (expr[1] * mod_mul_inv) % DECK_SIZE
    else:
        expr[1] = (expr[1] + int(v)) % DECK_SIZE

# q = QUERY
# base_expr = expr
# while N_STEPS:
#     expr_squared = [
#         (expr[0]*expr[0]) % DECK_SIZE,
#         (expr[0]*expr[1] + expr[1]) % DECK_SIZE
#     ]
#     expr = expr_squared
#     q = (expr[0]*q + expr[1]) % DECK_SIZE
#     if N_STEPS % 2:
#         q = (base_expr[0]*q + base_expr[1]) % DECK_SIZE
#     N_STEPS //= 2

# print(q)
# exit()

def run(x, expr, times):
    if times == 1:
        return (expr[0]*x + expr[1]) % DECK_SIZE
    
    expr_squared = [
        (expr[0]*expr[0]) % DECK_SIZE,
        (expr[0]*expr[1] + expr[1]) % DECK_SIZE
    ]
    ret = run(x, expr_squared, times//2)
    if times % 2 == 1:
        ret = (expr[0]*ret + expr[1]) % DECK_SIZE
    return ret

sol = run(QUERY, expr, N_STEPS)
print(sol)
