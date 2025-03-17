WIDTH = 25
HEIGHT = 6

img = input().strip()
layers = []

for x in range(0, len(img), WIDTH*HEIGHT):
    layers.append(img[x : x + WIDTH*HEIGHT])

mul = None
min_layer = None
min_zeros = len(img)
for layer in layers:
    n_zeros = layer.count("0")
    if n_zeros < min_zeros:
        min_zeros = n_zeros
        mul = layer.count("1") * layer.count("2")
        min_layer = layer

print(min_layer.count("1"), min_layer.count("2"), mul)
print(min_layer)