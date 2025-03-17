field = dict()

inc = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1)
}

def travel(wire_commands, wire_id, field):
    c_x, c_y = 0, 0
    total_steps_taken = 1
    
    for direction, max_steps in map(lambda x: (x[0], int(x[1:])), wire_commands):
        inc_x, inc_y = inc[direction]
        curr_steps_taken = 0
        while curr_steps_taken < max_steps:
            c_x += inc_x
            c_y += inc_y
            curr_steps_taken += 1
            if (c_x, c_y) not in field:
                field[c_x, c_y] = dict()
            if wire_id not in field[c_x, c_y]:
                field[c_x, c_y][wire_id] = total_steps_taken
            
            total_steps_taken += 1

wire1 = input().split(",")
wire2 = input().split(",")

travel(wire1, 1, field)
travel(wire2, 2, field)

min_dist = int(2e9)
sol_x, sol_y = int(1e9), int(1e9)
for x, y in field:
    w1_score = field[x, y].get(1)
    w2_score = field[x, y].get(2)
    if w1_score and w2_score:
        curr_dist = w1_score + w2_score
        if curr_dist < min_dist:
            sol_x, sol_y = x, y
            min_dist = curr_dist

print(sol_x, sol_y)
print(min_dist)