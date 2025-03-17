WIDTH = 25
HEIGHT = 6

img = input().strip()
sol = []

for i in range(0, WIDTH*HEIGHT):
    for layer_i in range(0, len(img), WIDTH * HEIGHT):
        if img[layer_i + i] != "2":
            sol.append(img[layer_i + i])
            break
for i in range(len(sol)):
    print("*" if sol[i]=="1" else " ", end = "" if (i+1) % WIDTH else "\n")