import algorithms.Node as node
import algorithms.Maze as maze
import algorithms.Algorithms as algos
import scenes.background as bg


class IDDFS(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.delay_time = 1
        self.depth_limit = 0  # current depth limit
        self.visited_count_last_depth = 0  #used to stored the number of visited nodes in the latest depth
        self.failed_attempts = 0
    def start(self):
        super().start()
        self.depth_limit = 0  # start from level 0
        self.visited_count_last_depth = 0  

        self.reset_iteration()

    def reset_iteration(self):
        self.stack = [node.Node(self.maze.initial_state(), depth = 0)]
        self.visited_nodes = set()

    def step(self):
        #avoid infinite loop when there's no goals/paths
        if not self.stack and self.running and not self.found_path:
            if len(self.visited_nodes) == self.visited_count_last_depth and self.failed_attempts == 20: #if the number of visited node remains the same and failed attempts reached 20, there's no path found
                self.running = False
                self.found_path = False
                return
            # if not, update the value and keep iterating
            self.visited_count_last_depth = len(self.visited_nodes)
            self.failed_attempts += 1
            self.depth_limit += 1
            self.reset_iteration()
            return
        
        if not self.stack or not self.running:
            return

        current_node = self.stack.pop()
        if current_node.state in self.visited_nodes:
            return

        bg.pygame.time.delay(self.delay_time)
        self.visited_nodes.add(current_node.state)
        self.visited_count += 1

        if self.maze.is_goal_state(current_node.state):
            self.found_path = True
            self.running = False
            self.reconstruct_path(current_node)
            return

        if current_node.depth < self.depth_limit:
            for neighbor, direction, cost in self.maze.get_neighbors(current_node.state):
                if neighbor not in self.visited_nodes:
                    self.stack.append(
                        node.Node(
                            state=neighbor,
                            parent=current_node,
                            action=direction,
                            path_cost=current_node.path_cost + cost,
                            depth=current_node.depth + 1
                        )
                    )
