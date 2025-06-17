class Node():
    
    def __init__(self, state, parent = None, action = None, path_cost = 0, 
                 depth = 0, heuristic = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = depth
        self.heuristic = heuristic

    def f(self):
        return self.path_cost + self.heuristic
    
    def g(self):
        return self.path_cost
    
    def h(self):
        return self.heuristic
    
    def __lt__(self, other):
        return self.f() < other.f()