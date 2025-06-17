import algorithms.Node as node
import algorithms.Algorithms as algos
import scenes.background as bg


class IDAStar(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.delay_time = 25
        self.threshold = 0
        self.next_threshold = float('inf')
        self.visited_count_last_threshold = 0
        self.failed_attempts = 0
        self.cost_type = 'F'
        self.cost_val = 0

    def start(self):
        super().start()
        initial_node = node.Node(
            state=self.maze.initial_state(),
            heuristic=self.maze.heuristic(self.maze.initial_state())
        )
        self.threshold = initial_node.heuristic
        self.next_threshold = float('inf')
        self.visited_count_last_threshold = 0
        self.failed_attempts = 0
        self.reset_iteration()

    def reset_iteration(self):
        initial_node = node.Node(
            state=self.maze.initial_state(),
            heuristic=self.maze.heuristic(self.maze.initial_state())
        )
        self.stack = [(initial_node, 0)]
        self.visited_nodes = set()
        self.visited_this_threshold = set()

    def step(self):
        if not self.stack and self.running and not self.found_path:
            if len(self.visited_nodes) == self.visited_count_last_threshold and self.failed_attempts == 20:
                self.running = False
                self.found_path = False
                return
            
            self.visited_count_last_threshold = len(self.visited_nodes)
            self.failed_attempts += 1
            self.threshold = self.next_threshold
            self.next_threshold = float('inf')
            self.reset_iteration()
            return
        
        if not self.stack or not self.running:
            return

        current_node, current_cost = self.stack.pop()
        
        if current_node.state in self.visited_this_threshold:
            return

        bg.pygame.time.delay(self.delay_time)
        self.visited_nodes.add(current_node.state)
        self.visited_this_threshold.add(current_node.state)
        self.visited_count += 1

        
        if self.maze.is_goal_state(current_node.state):
            self.found_path = True
            self.running = False
            self.reconstruct_path(current_node)
            return

        
        f_cost = current_cost + self.maze.heuristic(current_node.state)
        
        
        if f_cost > self.threshold:
            self.next_threshold = min(self.next_threshold, f_cost)
            return

        
        for neighbor_state, direction, cost in reversed(self.maze.get_neighbors(current_node.state)):
            if neighbor_state not in self.visited_this_threshold:
                neighbor_node = node.Node(
                    state=neighbor_state,
                    parent=current_node,
                    action=direction,
                    path_cost=current_cost + cost,
                    depth=current_node.depth + 1,
                    heuristic=self.maze.heuristic(neighbor_state)
                )
                self.stack.append((neighbor_node, current_cost + cost))