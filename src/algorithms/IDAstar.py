import algorithms.Node as node
import algorithms.Algorithms as algos
import scenes.background as bg


class IDAStar(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.delay_time = 1
        self.threshold = 0
        self.next_threshold = float('inf')
        self.visited_count_last_threshold = 0
        self.visited_costs = {}  # {(state): best g(n)}
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
        self.visited_costs = {}


    def step(self):
        if not self.stack and self.running and not self.found_path:
            if len(self.visited_nodes) == self.visited_count_last_threshold and self.failed_attempts == 20:
                self.running = False
                self.found_path = False
                return
            
            # Increment threshold if no path found
            self.visited_count_last_threshold = len(self.visited_nodes)
            self.failed_attempts += 1
            self.threshold = self.next_threshold
            self.next_threshold = float('inf')
            self.reset_iteration()
            return

        if not self.stack or not self.running:
            return

        current_node, current_cost = self.stack.pop()

        f_cost = current_cost + self.maze.heuristic(current_node.state)

        # If f_cost exceeds threshold, skip this node
        if f_cost > self.threshold:
            self.next_threshold = min(self.next_threshold, f_cost)
            return

        # If the node has been visited with a lower cost, skip it
        if current_node.state in self.visited_costs:
            if current_cost >= self.visited_costs[current_node.state]:
                return

        # Update visited costs and nodes
        self.visited_costs[current_node.state] = current_cost
        self.visited_nodes.add(current_node.state)
        self.visited_this_threshold.add(current_node.state)
        self.visited_count += 1

        bg.pygame.time.delay(self.delay_time)

        # Goal check
        if self.maze.is_goal_state(current_node.state):
            self.found_path = True
            self.running = False
            self.reconstruct_path(current_node)
            return

        # Mở rộng các hàng xóm
        for neighbor_state, direction, step_cost in reversed(self.maze.get_neighbors(current_node.state)):
            new_cost = current_cost + step_cost
            neighbor_node = node.Node(
                state=neighbor_state,
                parent=current_node,
                action=direction,
                path_cost=new_cost,
                depth=current_node.depth + 1,
                heuristic=self.maze.heuristic(neighbor_state)
            )
            self.stack.append((neighbor_node, new_cost))
