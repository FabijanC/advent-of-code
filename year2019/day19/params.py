import math

# pairs = [(12, 14), (13, 16), (14, 17), (15, 18), (16, 19), (17, 20), (18, 21), (19, 22)]
pairs = [(15, 18), (16, 19), (17, 20), (18, 21), (19, 22), (19, 23), (20, 24), (21, 25), (22, 26), (23, 27), (24, 28)]

for a in range(1, 100):
    for b in range(1, 100):
        for c in range(1, 100):
            for x, y in pairs:
                if math.floor(x*a/b) + c != y:
                    break
            else:
                print(a, b, c)
