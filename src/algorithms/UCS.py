import algorithms.Node as node
import algorithms.Maze as maze
import algorithms.Algorithms as algos
import scenes.background as bg
import heapq
import heapq

class UCS(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.pq = []
        self.current_cost = {}
        self.delay_time = 10  # delay time in milliseconds for visualization
        self.cost_type = 'G'
        self.cost_val = 0
        self.direction_priority = ['RIGHT', 'DOWN', 'LEFT', 'UP']

    def start(self):
        super().start()
        self.pq = []
        self.current_cost = {}
        start_state = self.maze.initial_state()
        start_node = node.Node(state=start_state, path_cost=0, heuristic=0)
        heapq.heappush(self.pq, (0, 0, start_node))  # (path_cost, priority_value, node)
        self.current_cost[start_state] = 0

    def step(self):
        if not self.running or len(self.pq) == 0:
            self.found_path = False
            self.running = False
            return

        _, _, current_node = heapq.heappop(self.pq)

        if current_node.state in self.visited_nodes:
            return

        bg.pygame.time.delay(self.delay_time)
        self.visited_nodes.add(current_node.state)
        self.cost_val = current_node.path_cost
        self.visited_count += 1
        self.current_node = current_node

        if self.maze.is_goal_state(current_node.state):
            self.found_path = True
            self.running = False
            self.reconstruct_path(current_node)
            return

        for neighbor_state, direction, cost in self.maze.get_neighbors(current_node.state):
            new_cost = current_node.path_cost + cost

            if (neighbor_state not in self.current_cost) or (new_cost < self.current_cost[neighbor_state]):
                self.current_cost[neighbor_state] = new_cost

                # Get priority index based on direction
                try:
                    dir_priority = self.direction_priority.index(direction)
                except ValueError:
                    dir_priority = len(self.direction_priority)  # fallback if direction not in list

                neighbor_node = node.Node(
                    state=neighbor_state,
                    parent=current_node,
                    action=direction,
                    path_cost=new_cost,
                    depth=current_node.depth + 1,
                    heuristic=0
                )

                heapq.heappush(self.pq, (new_cost, dir_priority, neighbor_node))

       