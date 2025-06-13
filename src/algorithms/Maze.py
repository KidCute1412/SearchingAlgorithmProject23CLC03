class Maze():
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if self.rows > 0 else 0
        self.start = self.find('S')
        self.end = self.find('E')
        print(self.rows, self.cols)

    def find(self, value):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze[row][col] == value:
                    return (row, col)
        return None

    def initial_state(self):
        return self.start
    
    def goal_state(self):
        return self.end
    
    def is_goal_state(self, state):
        return self.end == state

    def in_bounds(self, state):
        row, col = state
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def walkable(self, state):
        row, col = state
        return self.maze[row][col] != '0'
    
    
    def get_neighbors(self, state):
        row, col = state
        neighbors = []
        directions = {'UP': (-1, 0),
                      'DOWN': (1, 0),
                      'RIGHT': (0, 1),                       
                      'LEFT': (0, -1),
                    }
        for direction, (dr, dc) in directions.items():
            new_row, new_col = row + dr, col + dc
            new_state = (new_row, new_col)
            if self.in_bounds(new_state):
                if self.walkable(new_state):
                    neighbors.append((new_state, direction, 1)) # cost is 1
        
        return neighbors
    
    def heuristic(self, state):
        if not self.end:
            return 0
        row, col = state
        end_row, end_col = self.end
        return abs(row - end_row) + abs(col - end_col) # Manhattan distance
    
    def __str__(self):
        return '\n'.join(''.join(row) for row in self.maze)

                
        