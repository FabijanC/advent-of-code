OPEN = '.'
START = '@'
WALL = '#'

UP, DOWN, LEFT, RIGHT = (-1,0), (1,0), (0,-1), (0,1)
delta2lateral = {
    UP: (LEFT, RIGHT),
    DOWN: (RIGHT, LEFT),
    LEFT: (DOWN, UP),
    RIGHT: (UP, DOWN)
}
DELTAS = list(delta2lateral.keys())

INF = int(1e9)

'''
    area[new_pos] is presumed to be OPEN.
    returns pos of next crossroad and steps it took to get there
    steps_taken is set to None if dead end encountered
'''
def move(area, new_pos, delta):
    di, dj = delta
    ni, nj = new_pos
    steps_taken = 1
    while True:
        forward_i, forward_j = ni + di, nj + dj
        forward_val = area[forward_i][forward_j]

        left, right = delta2lateral[di, dj]
        left_i, left_j = ni + left[0], nj + left[1]
        left_val = area[left_i][left_j]

        right_i, right_j = ni + right[0], nj + right[1]
        right_val = area[right_i][right_j]
        
        if forward_val == WALL:
            if left_val == WALL:
                if right_val == WALL:
                    steps_taken = None
                    break
                elif right_val == OPEN:
                    ni, nj = right_i, right_j
                    di, dj = right
                    steps_taken += 1
                    continue
                elif right_val.isalpha():
                    ni, nj = right_i, right_j
                    steps_taken += 1
                    break
                else:
                    raise ValueError("invalid state")
            
            elif left_val == OPEN:
                if right_val == WALL:
                    ni, nj = left_i, left_j
                    di, dj = left
                    steps_taken += 1
                    continue
                else:
                    break
            
            elif left_val.isalpha():
                if right_val == WALL:
                    ni, nj = left_i, left_j # just turn
                    steps_taken += 1
                    break
                else:
                    break
            
        elif forward_val == OPEN:
            if left_val == WALL and right_val == WALL:
                ni, nj = forward_i, forward_j
                steps_taken += 1
                continue
            else:
                break
        
        elif forward_val.isalpha():
            if left_val == WALL and right_val == WALL:
                ni, nj = forward_i, forward_j
                steps_taken += 1
                break
            else:
                break

        raise ValueError("invalid area value")
    
    return (ni, nj), steps_taken

def get_neighbors(start_pos, area):
    source_kind = area[start_pos[0]][start_pos[1]]
    neighbors = {}
    stack = [(start_pos, 0)]
    visited = {}
    while stack:
        pos, dist = stack.pop()
        i, j = pos
        kind = area[i][j]
        if kind.isalpha() and kind != source_kind: # or kind == START
            neighbors[kind] = dist # TODO be careful!!! ord(kind)
            continue
        if kind == WALL:
            continue
        if visited.get(pos, INF) <= dist:
            continue
        visited[pos] = dist
        for di, dj in DELTAS:
            new_pos = i+di, j+dj
            stack.append((new_pos, dist+1))
    
    return neighbors

def make_graph(start_pos, area, nodes):
    stack = [start_pos]
    visited = set()
    while stack:
        pos = i, j = stack.pop()
        visited.add(pos)
        neighbors = {}
        for delta in delta2lateral:
            di, dj = delta
            ni, nj = i + di, j + dj
            nval = area[ni][nj]
            if nval == WALL:
                continue
            elif nval == OPEN:
                new_pos, steps_taken = move(area, (ni, nj), delta)
                ni, nj = new_pos
                if steps_taken is None:
                    continue
                neighbors[new_pos] = steps_taken
            elif nval.isalpha():
                neighbors[ni, nj] = 1
            else:
                raise ValueError(f"Unknown type at {ni, nj}: {nval}")

            if (ni, nj) not in visited:
                stack.append((ni, nj))
        
        nodes[pos] = neighbors