import algorithms.Node as node
import algorithms.Algorithms as algos
import scenes.background as bg
from collections import deque

class BFS(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.delay_time = 20  # delay time in milliseconds for visualization

    def start(self):
        super().start()
        self.queue = deque([node.Node(self.maze.initial_state())])
        return None

    def step(self):
        if not self.queue or not self.running:
            self.found_path = False
            self.running = False
            return

        current_node = self.queue.popleft()

        if current_node.state in self.visited_nodes:
            return

        bg.pygame.time.delay(self.delay_time)  # Visual delay
        self.visited_nodes.add(current_node.state)
        self.visited_count += 1

        # Goal found
        if self.maze.is_goal_state(current_node.state):
            self.found_path = True
            self.running = False
            self.reconstruct_path(current_node)
            return

        # Retrieve and prioritize neighbors
        neighbors = self.maze.get_neighbors(current_node.state)

        # Optional: sort by direction priority (RIGHT, DOWN, LEFT, UP)
        direction_priority = ['RIGHT', 'DOWN', 'LEFT', 'UP']
        neighbors.sort(key=lambda x: direction_priority.index(x[1]))

        for neighbor_state, direction, cost in neighbors:
            if neighbor_state not in self.visited_nodes:
                new_node = node.Node(neighbor_state, current_node, path_cost=current_node.path_cost + cost)
                self.queue.append(new_node)

        

