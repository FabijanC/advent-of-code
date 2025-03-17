field = dict()

inc = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1)
}

def travel(wire_commands, wire_id, field):
    c_x, c_y = 0, 0
    
    for direction, max_steps in map(lambda x: (x[0], int(x[1:])), wire_commands):
        inc_x, inc_y = inc[direction]
        steps_taken = 0
        while steps_taken < max_steps:
            c_x += inc_x
            c_y += inc_y
            if (c_x, c_y) not in field:
                field[c_x, c_y] = dict()
            if wire_id not in field[c_x, c_y]:
                field[c_x, c_y][wire_id] = 0
            field[c_x, c_y][wire_id] += 1
            
            steps_taken += 1

wire1 = input().split(",")
wire2 = input().split(",")

travel(wire1, 1, field)
travel(wire2, 2, field)

min_dist = int(2e9)
sol_x, sol_y = int(1e9), int(1e9)
for x, y in field:
    if field[x, y].get(1) and field[x,y].get(2):
        curr_dist = abs(x) + abs(y)
        if curr_dist < min_dist:
            sol_x, sol_y = x, y
            min_dist = curr_dist

print(sol_x, sol_y)
print(min_dist)