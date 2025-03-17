DIR_UP = 0,1
DIR_DOWN = 0,-1
DIR_LEFT = -1,0
DIR_RIGHT = 1,0

DIRS = [DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT]
NUM_DIRS = len(DIRS)

WAITING_FOR_COLOR = 0
WAITING_FOR_DIRECTION = 1

COLOR_SYMBOL = ['.', '#']

INF = int(1e9)

class Robot:
    def __init__(self):
        self.panels = {}
        self.pos = 0, 0
        self.dir = DIRS.index(DIR_UP)
        self.panels[self.pos] = 1
        self.state = WAITING_FOR_COLOR
    
    def get_current_color(self):
        return self.panels.get(self.pos, 0)
    
    def progress(self, val):
        if self.state == WAITING_FOR_COLOR:
            self.panels[self.pos] = val
        
        elif self.state == WAITING_FOR_DIRECTION:
            if val == 0: val = -1
            self.dir = (self.dir + val + NUM_DIRS) % NUM_DIRS
            dx, dy = DIRS[self.dir]
            self.pos = self.pos[0] + dx, self.pos[1] + dy
            
        self.state = 1 - self.state
    
    def get_num_painted(self):
        return len(self.panels)
    
    def show_painting(self):
        min_x = min_y = INF
        max_x = max_y = -INF
        for key in self.panels:
            min_x = min(min_x, key[0])
            max_x = max(max_x, key[0])
            min_y = min(min_y, key[1])
            max_y = max(max_y, key[1])
        
        rows = []
        for x in range(min_x, max_x+1):
            curr_row = []
            for y in range(min_y, max_y+1):
                symbol = COLOR_SYMBOL[self.panels.get((x,y), 0)]
                curr_row.append(symbol)
            rows.append("".join(curr_row))
        return "\n".join(rows)