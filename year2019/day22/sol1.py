import sys
from collections import deque

def cut(deck: deque, val: int):
    if val > 0:
        for _ in range(val):
            deck.append(deck.popleft())
    else:
        for _ in range(-val):
            deck.appendleft(deck.pop())
    return deck

def deal_with_increment(deck:deque, inc:int):
    deck_size = len(deck)
    new_deck = [-1 for _ in range(deck_size)]
    i = 0
    for val in deck:
        new_deck[i] = val
        i = (i + inc) % deck_size
    
    return deque(new_deck)

# TEST
# DECK_SIZE = 10
# print(cut(deque(range(DECK_SIZE)), 3))
# print(cut(deque(range(DECK_SIZE)), -4))
# deck = deque(range(DECK_SIZE))
# print(deck)
# deck = deal_with_increment(deck, 3)
# print(deck)
# deck = deal_with_increment(deck, 3)
# print(deck)
# deck = deal_with_increment(deck, 3)
# print(deck)
# deck = deal_with_increment(deck, 3)
# print(deck)
# deck = deal_with_increment(deck, 3)
# print(deck)
# exit()

with open(sys.argv[1]) as f:
    lines = f.read().strip().split("\n")

# DECK_SIZE = 10007
DECK_SIZE = 10

deck = deque(range(DECK_SIZE))
for line in lines:
    print(deck)
    if line == "deal into new stack":
        deck.reverse()
        continue
    technique, val = line.rsplit(" ", 1)
    val = int(val)
    technique = technique.replace(" ", "_")
    deck = globals()[technique](deck, val)
QUERY = 2019
print(deck)#print(deck.index(QUERY))