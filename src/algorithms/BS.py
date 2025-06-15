import algorithms.Node as node
import algorithms.Algorithms as algos
import scenes.background as bg

class BS(algos.searching_algorithms):
    def __init__(self, beam_width=10):
        super().__init__()
        self.beam_width = beam_width
        self.delay_time = 50  # delay time in milliseconds for visualization

    def start(self):
        super().start()
        self.queue = [node.Node(self.maze.initial_state())]

    def step(self):
        if not self.queue or not self.running:
            return

        next_level = []

        for current_node in self.queue:
            if current_node.state in self.visited_nodes:
                continue

            bg.pygame.time.delay(self.delay_time)
            self.visited_nodes.add(current_node.state)
            self.visited_count += 1
            if self.maze.is_goal_state(current_node.state):
                self.found_path = True
                self.running = False
                self.reconstruct_path(current_node)
                self.stop_timer()
                return

            for neighbor, direction, cost in self.maze.get_neighbors(current_node.state):
                if neighbor not in self.visited_nodes:
                    child_node = node.Node(neighbor, current_node)
                    next_level.append(child_node)

        # Sắp xếp theo heuristic và giữ lại beam_width node tốt nhất
        next_level.sort(key=lambda n: self.maze.heuristic(n.state))
        self.queue = next_level[:self.beam_width]
