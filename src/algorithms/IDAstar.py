import algorithms.Node as node
import algorithms.Algorithms as algos
import scenes.background as bg


class IDAStar(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.delay_time = 50  # delay time in milliseconds for visualization

    def start(self):
        super().start()
        self.start_node = node.Node(self.maze.initial_state())
        self.end_node = self.maze.goal_state()
        self.threshold = self.maze.heuristic(self.start_node.state)
        self.path = []
        self.visited_nodes = set()
        self.running = True
        self.stack = [(self.start_node, 0)]
        self.next_threshold = float('inf')
        self.visited_this_threshold = set()
        self.solution_found = False

    def step(self):
        if not self.running or self.solution_found:
            return

        while self.stack:
            current_node, g = self.stack.pop()

            f = g + self.maze.heuristic(current_node.state)
            if f > self.threshold:
                self.next_threshold = min(self.next_threshold, f)
                continue

            if current_node.state in self.visited_this_threshold:
                continue

            self.visited_nodes.add(current_node.state)
            self.visited_this_threshold.add(current_node.state)
            self.visited_count += 1
            bg.pygame.time.delay(self.delay_time)

            if self.maze.is_goal_state(current_node.state):
                self.running = False
                self.solution_found = True
           
                self.reconstruct_path(current_node)
                return

            for neighbor_state, direction, cost in reversed(self.maze.get_neighbors(current_node.state)):
                if neighbor_state not in self.visited_this_threshold:
                    neighbor_node = node.Node(neighbor_state, current_node, direction,
                                            path_cost=g + cost,
                                            depth=current_node.depth + 1,
                                            heuristic=self.maze.heuristic(neighbor_state))
                    self.stack.append((neighbor_node, g + cost))

            return 

        
        if not self.solution_found:
            if self.next_threshold == float('inf'):
                self.running = False
                return

            self.threshold = self.next_threshold
            self.next_threshold = float('inf')

            self.stack = [(node.Node(self.maze.initial_state()), 0)]

            self.visited_this_threshold = set()
            self.visited_nodes = set()


    

