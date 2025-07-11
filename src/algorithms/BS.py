from os import path
import algorithms.Node as node
import algorithms.Algorithms as algos
import scenes.background as bg

class BS(algos.searching_algorithms):
    def __init__(self, beam_width=10):
        super().__init__()
        self.beam_width = beam_width
        self.delay_time = 100  # delay time in milliseconds for visualization
        self.cost_type = 'H'
        self.cost_val = 0

    def start(self):
        super().start()
        self.queue = [node.Node(self.maze.initial_state())]

    def step(self):
        if not self.queue or not self.running:
            self.found_path = False
            self.running = False
            return

        next_level = []
        bg.pygame.time.delay(self.delay_time)
        for current_node in self.queue:
            if current_node.state in self.visited_nodes:
                continue

            
            self.visited_nodes.add(current_node.state)
            self.visited_count += 1
            if self.maze.is_goal_state(current_node.state):
                self.found_path = True
                self.running = False
                self.reconstruct_path(current_node)
      
                return

            for neighbor, direction, cost in self.maze.get_neighbors(current_node.state):
                if neighbor not in self.visited_nodes:
                    child_node = node.Node(neighbor, current_node, path_cost=current_node.path_cost + cost)
                    next_level.append(child_node)

    
        next_level.sort(key=lambda n: self.maze.heuristic(n.state))
        self.queue = next_level[:self.beam_width]
