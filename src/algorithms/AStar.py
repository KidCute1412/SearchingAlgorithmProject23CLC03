import algorithms.Node as node
import algorithms.Algorithms as algos
import scenes.background as bg






class AStar(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.open_set = set()
        self.closed_set = set()
        self.delay_time = 50 # delay time in milliseconds for visualization

    def start(self):
        super().start()
        self.open_set.add(node.Node(self.maze.initial_state()))
        return None

    def step(self):
        if not self.running or not self.open_set:
            self.found_path = False
            self.running = False
            return
        
        current_node = min(self.open_set, key=lambda n: n.path_cost + n.heuristic)
        self.open_set.remove(current_node)
        
        if current_node.state in self.visited_nodes:
            return
        
        bg.pygame.time.delay(self.delay_time)  # Add a delay to visualize the A* process
        self.visited_nodes.add(current_node.state)
        self.visited_count += 1
        self.current_node = current_node
        
        # reached goal
        if self.maze.is_goal_state(current_node.state):
            self.found_path = True
            self.running = False
            self.reconstruct_path(current_node)
            return
        
        # neighbour nodes
        for neighbor_state, action, cost in self.maze.get_neighbors(current_node.state):
            neighbor_node = node.Node(
                state=neighbor_state,
                parent=current_node,
                action=action,
                path_cost=current_node.path_cost + cost,
                depth=current_node.depth + 1,
                heuristic=self.maze.heuristic(neighbor_state)
            )
            
            if neighbor_state not in self.closed_set or neighbor_node.path_cost < current_node.path_cost:
                self.open_set.add(neighbor_node)
        
        self.closed_set.add(current_node.state)