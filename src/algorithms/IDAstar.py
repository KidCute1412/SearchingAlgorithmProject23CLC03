import algorithms.Node as node
import algorithms.Maze as maze
import algorithms.Algorithms as algos
import scenes.background as bg

class IDAStar(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.visited_start = set()
        self.path = []
        self.running = False
        self.found_path = False
        self.threshold = 0
        self.min_threshold = float('inf')
        self.stack = []
        
    def start(self):
        super().start()
        self.visited_start = set()
        self.path = []
        self.running = True
        self.found_path = False
        start_node = node.Node(
            state=self.maze.initial_state(),
            heuristic=self.maze.heuristic(self.maze.initial_state())
        )
        self.threshold = start_node.heuristic
        self.stack = [start_node]
        
    def step(self):
        if not self.running:
            return
            
        if not self.stack:
            # Threshold reached, start new iteration with increased threshold
            self.threshold = self.min_threshold
            self.min_threshold = float('inf')
            start_node = node.Node(
                state=self.maze.initial_state(),
                heuristic=self.maze.heuristic(self.maze.initial_state())
            )
            self.stack = [start_node]
            self.visited_start = set()
            return
            
        current_node = self.stack.pop()
        
        if current_node.state in self.visited_start:
            return
            
        self.visited_start.add(current_node.state)
        bg.pygame.time.delay(50)  # Visualization delay
        
        # Check for goal state
        if self.maze.is_goal_state(current_node.state):
            self.found_path = True
            self.running = False
            self.reconstruct_path(current_node)
            return
            
        # Calculate f-cost (g + h)
        f_cost = current_node.path_cost + current_node.heuristic
        
        if f_cost > self.threshold:
            self.min_threshold = min(self.min_threshold, f_cost)
            return
            
        # Explore neighbors in reverse order to maintain proper stack ordering
        neighbors = self.maze.get_neighbors(current_node.state)
        for neighbor, direction, cost in reversed(neighbors):
            if neighbor not in self.visited_start:
                new_heuristic = self.maze.heuristic(neighbor)
                new_node = node.Node(
                    state=neighbor,
                    parent=current_node,
                    action=direction,
                    path_cost=current_node.path_cost + cost,
                    heuristic=new_heuristic
                )
                self.stack.append(new_node)
                
    def reconstruct_path(self, current_node):
        """Reconstruct the path from goal to start"""
        self.path = []
        while current_node:
            self.path.append(current_node.state)
            current_node = current_node.parent
        self.path.reverse()  # Reverse to get start-to-goal order