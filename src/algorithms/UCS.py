import algorithms.Node as node
import algorithms.Maze as maze
import algorithms.Algorithms as algos
import scenes.background as bg
import heapq
class USC(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.pq = []
        self.cost_so_far = {}

    def start(self):
        super().start()
        start_state = self.maze.initial_state()
        start_node = node.Node(state=start_state, path_cost=0)
        heapq.heappush(self.pq, (start_node.path_cost, start_node))
        self.cost_so_far[start_state] = 0

    def step(self):
        if not self.running or not self.pq:
            return

        _, current_node = heapq.heappop(self.pq)

        # avoid repetition
        if current_node.state in self.visited_nodes:
            return

        bg.pygame.time.delay(100)  
        self.visited_nodes.add(current_node.state)
        self.current_node = current_node  

        # reached goal
        if self.maze.is_goal_state(current_node.state):
            self.found_path = True
            self.running = False
            self.reconstruct_path(current_node)
            return

        # neighbour nodes
        for neighbor_state, action, step_cost in self.maze.get_neighbors(current_node.state):
            new_cost = current_node.path_cost + step_cost

            if (neighbor_state not in self.cost_so_far) or (new_cost < self.cost_so_far[neighbor_state]):
                self.cost_so_far[neighbor_state] = new_cost
                neighbor_node = node.Node(
                    state=neighbor_state,
                    parent=current_node,
                    action=action,
                    path_cost=new_cost,
                    depth=current_node.depth + 1
                )
                heapq.heappush(self.pq, (new_cost, neighbor_node))
       