import sys

lines = [line.strip() for line in sys.stdin]

numbers = [int(n) for n in lines[0].split(",")]

SIZE = 5
BUFFER_LINES = 1
cards = []
for top_line_i in range(2, len(lines), SIZE + BUFFER_LINES):
    card_lines = lines[top_line_i : top_line_i + SIZE]
    card = []
    for card_line in card_lines:
        card.append([int(n) for n in card_line.split()])
    cards.append(card)

def marked(val):
    return val is None

def wins_row(card, i):
    return all(map(marked, card[i]))

def wins_col(card, j):
    for i in range(SIZE):
        if not marked(card[i][j]):
            return False
    return True

def sum_remaining(card):
    rem_sum = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if card[i][j] is not None:
                rem_sum += card[i][j]
    return rem_sum

card2place = {}
card2score = {}
for number in numbers:
    for card_i, card in enumerate(cards):
        card_i += 1
        if card_i in card2place:
            continue
        for i in range(SIZE):
            for j in range(SIZE):
                if card[i][j] != number:
                    continue
                card[i][j] = None
                if wins_row(card, i) or wins_col(card, j):
                    rem_sum = sum_remaining(card)
                    score = number * rem_sum
                    card2place[card_i] = len(card2place) + 1
                    card2score[card_i] = score

max_card = None
max_place = 0
for card in card2place:
    place = card2place[card]
    if place > max_place:
        max_place = place
        max_card = card

print(card2score[max_card])
