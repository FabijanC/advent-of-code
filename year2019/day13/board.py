import readchar

INF = int(1e9)

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

class Board:
    def __init__(self):
        self.mapping = {}
        self.num2char = [
            " ", # EMPTY
            "#", # WALL
            ".", # BLOCK
            "^", # PADDLE
            "O", # BALL
        ]
        self.switched = False
        self.ball_pos = None
        self.paddle_pos = None
    
    def put(self, pos, val):
        x, y = pos
        if val == BALL:
            self.ball_pos = pos
        elif val == PADDLE:
            self.paddle_pos = pos
        # if self.switched:
        #     if val == EMPTY and self.matrix[y][x] == BLOCK:
        #         self.blocks_broken += 1
        #         self.last_broken = x, y
        #     self.matrix[y][x] = val
        #     if val == PADDLE:
        #         self.paddle_move_cnt += 1
        #     elif val == BALL:
        #         self.ball_move_cnt += 1
        # else:
        self.mapping[pos] = val
        
    
    def switch_to_matrix(self):
        assert not self.switched
        self.switched = True
        self.min_x = self.min_y = INF
        self.max_x = self.max_y = -INF
        for key in self.mapping:
            self.min_x = min(self.min_x, key[0])
            self.min_y = min(self.min_y, key[1])
            self.max_x = max(self.max_x, key[0])
            self.max_y = max(self.max_y, key[1])
        
        assert self.min_x == 0
        assert self.min_y == 0
        self.matrix = [[None for _ in range(self.max_x+1)] for _ in range(self.max_y+1)]
        for x, y in self.mapping:
            val = self.mapping[x,y]
            self.matrix[y][x] = val

    def get_input(self):
        '''
        THIS IS THE SMART SOLUTION (not mine)
        if self.paddle_pos[0] < self.ball_pos[0]:
            return 1
        elif self.paddle_pos[0] == self.ball_pos[1]:
            return 0
        return -1
        '''
        ret = None
        while ret is None:
            command = readchar.readkey()
            if command == "a":
                ret = -1
            elif command == "s":
                ret = 0
            elif command == "d":
                ret = 1
        return ret
        
    
    def display(self):
        out = []
        for y in range(self.max_y):
            r = range(self.max_x)
            row = map(lambda x: self.num2char[self.matrix[y][x]], r)
            out.append("".join(row))
        return "\n".join(out)
    