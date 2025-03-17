UP = "^"
DOWN = "_"
ILLEGAL_PATTERNS = [DOWN*4]

def rek(sofar, arr):
    if len(sofar) == 9:
        for pattern in ILLEGAL_PATTERNS:
            if pattern in sofar or sofar[3] == DOWN:
                break
        else:
            arr.append(sofar)
        return
    rek(sofar+UP, arr)
    rek(sofar+DOWN, arr)

arr = []
rek("", arr)
print(len(arr))

new_arr = []
for i, a in enumerate(arr):
    c = "\0"
    print(i+1, a)
    while c not in "yn":
        c = input().lower()
    
    if c == "y":
        new_arr.append(a)

print(new_arr)
print(len(new_arr))