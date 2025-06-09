import algorithms.Node as node
import algorithms.Maze as maze
import algorithms.Algorithms as algos
import scenes.background as bg
import heapq

class BS(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.beam_width = 3  # Number of nodes to keep at each level
        self.current_level = []
        self.next_level = []
        self.path = []
        self.running = False
        self.found_path = False

    def start(self):
        super().start()
        # Initialize with start node
        start_node = node.Node(
            state=self.maze.initial_state(),
            heuristic=self.maze.heuristic(self.maze.initial_state())
        )
        self.current_level = [start_node]
        self.path = []
        self.running = True
        self.found_path = False

    def step(self):
        if not self.running or not self.current_level:
            return

        self.next_level = []
        
        # Process all nodes in current level
        for current_node in self.current_level:
            if current_node.state in self.visited_start:
                continue

            # Mark as visited
            self.visited_start.add(current_node.state)
            bg.pygame.time.delay(50)  # Visualization delay

            # Check for goal state
            if self.maze.is_goal_state(current_node.state):
                self.found_path = True
                self.running = False
                self.reconstruct_path(current_node)
                return

            # Expand neighbors
            for neighbor, direction, cost in self.maze.get_neighbors(current_node.state):
                if neighbor not in self.visited_start:
                    heuristic = self.maze.heuristic(neighbor)
                    new_node = node.Node(
                        state=neighbor,
                        parent=current_node,
                        action=direction,
                        path_cost=current_node.path_cost + cost,
                        heuristic=heuristic
                    )
                    self.next_level.append(new_node)

        # Select top-k nodes for next level based on heuristic
        self.next_level.sort(key=lambda x: x.heuristic)
        self.current_level = self.next_level[:self.beam_width]

    def reconstruct_path(self, current_node):
        """Reconstruct the path from goal to start"""
        self.path = []
        while current_node:
            self.path.append(current_node.state)
            current_node = current_node.parent
        self.path.reverse()  # Reverse to get start-to-goal order