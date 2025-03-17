
EPS = 1e-6

class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return self.x == other.x and self.y == other.y
    
    def dist(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** .5
    
    def __str__(self):
        return f"A({self.x},{self.y})"
    
    def __repr__(self):
        return self.__str__()

class DirectedLine:
    """
        y - y1 = (y2 - y1) / (x2 - x1) * (x - x1)
        (y - y1) * (x2 - x1) = (y2 - y1) * (x - x1)
    """
    def __init__(self, a1, a2):
        self.a1 = a1
        self.a2 = a2
        self.length = a1.dist(a2)

    def __contains__(self, other):
        return abs(self.a1.dist(other) + self.a2.dist(other) - self.length) < EPS
    
    def __len__(self):
        return self.length