import algorithms.Node as node
import algorithms.Maze as maze
import algorithms.Algorithms as algos
import scenes.background as bg

class BFS(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.queue = []       
        self.path = []          # Final path storage
        self.running = False    # Search status flag
        self.found_path = False # Path found flag

    def start(self):
        super().start()
        # Create initial node and add to queue
        start_node = node.Node(self.maze.initial_state())
        self.queue = [start_node]
        self.path = []
        self.running = True
        self.found_path = False

    def step(self):
        if not self.running or not self.queue:
            return

        # Get next node from queue (FIFO)
        current_node = self.queue.pop(0)
        
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
                # Create new node and add to queue
                new_node = node.Node(
                    state=neighbor,
                    parent=current_node,
                    action=direction,
                    path_cost=current_node.path_cost + cost
                )
                self.queue.append(new_node)

    def reconstruct_path(self, current_node):
        """Reconstruct the path from goal back to start"""
        self.path = []
        while current_node:
            self.path.append(current_node.state)
            current_node = current_node.parent
        self.path.reverse()  # Reverse to get start-to-goal order