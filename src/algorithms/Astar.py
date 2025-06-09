import algorithms.Node as node
import algorithms.Maze as maze
import algorithms.Algorithms as algos
import scenes.background as bg
import heapq  # For priority queue implementation

class AStar(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.priority_queue = []
        self.path = []
        self.running = False
        self.found_path = False
        
    def start(self):
        super().start()
        # Initialize priority queue with start node
        start_node = node.Node(
            state=self.maze.initial_state(),
            heuristic=self.maze.heuristic(self.maze.initial_state())
        )
        heapq.heappush(self.priority_queue, start_node)
        self.path = []
        self.running = True
        self.found_path = False

    def step(self):
        if not self.running or not self.priority_queue:
            return
            
        current_node = heapq.heappop(self.priority_queue)
        
        # Skip if already visited
        if current_node.state in self.visited_start:
            return
            
        # Mark as visited
        self.visited_start.add(current_node.state)
        
        # Visualization delay
        bg.pygame.time.delay(50)
        
        # Check for goal state
        if self.maze.is_goal_state(current_node.state):
            self.found_path = True
            self.running = False
            self.reconstruct_path(current_node)
            return
            
        # Explore neighbors
        for neighbor, direction, cost in self.maze.get_neighbors(current_node.state):
            if neighbor not in self.visited_start:
                # Calculate total cost (g(n) + h(n))
                new_cost = current_node.path_cost + cost
                heuristic = self.maze.heuristic(neighbor)
                
                new_node = node.Node(
                    state=neighbor,
                    parent=current_node,
                    action=direction,
                    path_cost=new_cost,
                    heuristic=heuristic
                )
                # Add to priority queue
                heapq.heappush(self.priority_queue, new_node)
                
    def reconstruct_path(self, current_node):
        """Reconstruct the path from goal to start"""
        self.path = []
        while current_node:
            self.path.append(current_node.state)
            current_node = current_node.parent
        self.path.reverse()  # Reverse to get start-to-goal order