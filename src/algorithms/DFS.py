import algorithms.Node as node
import algorithms.Algorithms as algos
import scenes.background as bg


class DFS(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.delay_time = 50  # delay time in milliseconds for visualization
    def start(self):
        super().start()
        self.stack = [node.Node(self.maze.initial_state())]
        return None

    def step(self):
        if not self.stack or not self.running:
            self.found_path = False
            self.running = False
            return
        current_node = self.stack.pop()
        if current_node.state in self.visited_nodes:
            return
        bg.pygame.time.delay(self.delay_time)  # Add a delay to visualize the DFS process
        self.visited_nodes.add(current_node.state)
        self.visited_count += 1
        # found goal
        if self.maze.is_goal_state(current_node.state):
            self.found_path = True
            self.running = False
            self.reconstruct_path(current_node)
            
        
        for neighbor, direction, cost in self.maze.get_neighbors(current_node.state):
            if neighbor not in self.visited_nodes:
                self.stack.append(node.Node(neighbor, current_node, path_cost=current_node.path_cost + cost))
        

