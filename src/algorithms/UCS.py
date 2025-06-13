import algorithms.Node as node
import algorithms.Maze as maze
import algorithms.Algorithms as algos
import scenes.background as bg
import heapq
class USC(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.pq = []
        self.current_cost = {}
        self.delay_time = 10  # delay time in milliseconds for visualization

    def start(self):
        super().start()
        self.pq = []
        self.current_cost = {}
        start_state = self.maze.initial_state()
        start_node = node.Node(state = start_state, path_cost = 0, heuristic = 0)
        heapq.heappush(self.pq, (start_node.path_cost, start_node))
        self.current_cost[start_state] = 0

    def step(self):
        if not self.running or not self.pq:
            return
        
        _, current_node = heapq.heappop(self.pq) #take out the node with smallest cost

        # avoid repetition
        if current_node.state in self.visited_nodes:
            return

        bg.pygame.time.delay(self.delay_time)  
        self.visited_nodes.add(current_node.state)
        self.visited_count += 1
        self.current_node = current_node  

        # reached goal
        if self.maze.is_goal_state(current_node.state):
            self.found_path = True
            self.running = False
            self.stop_timer()
            self.reconstruct_path(current_node)
            return

        # neighbour nodes
        for neighbour_state, action, cost in self.maze.get_neighbors(current_node.state):
            new_cost = current_node.path_cost + cost

            if (neighbour_state not in self.current_cost) or (new_cost < self.current_cost[neighbour_state]):
                self.current_cost[neighbour_state] = new_cost
                neighbor_node = node.Node(
                    state = neighbour_state,
                    parent = current_node,
                    action = action,
                    path_cost = new_cost,
                    depth=current_node.depth + 1,
                    heuristic=0
                )
                heapq.heappush(self.pq, (new_cost, neighbor_node))
       