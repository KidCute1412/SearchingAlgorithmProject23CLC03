import algorithms.Node as node
import algorithms.Algorithms as algos
import scenes.background as bg

class BDS(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.delay_time = 10  # delay time in milliseconds for visualization

    def start(self):
        super().start()
        self.frontier_start = [node.Node(self.maze.initial_state())]
        self.frontier_goal = [node.Node(self.maze.goal_state())]
        self.visited_start = {}
        self.visited_goal = {}
        self.visited_nodes = set()  
        self.meeting_node = None
        return None

    def step(self):
        if not self.running or (not self.frontier_start and not self.frontier_goal):
            return
        bg.pygame.time.delay(self.delay_time) # delay for visualization
        def expand_frontier(frontier, visited_this, visited_other):
            if not frontier:
                return None
            current_node = frontier.pop(0)
            if current_node.state in visited_this:
                return None

            visited_this[current_node.state] = current_node
            self.visited_nodes.add(current_node.state)
            self.visited_count += 1
            

            # Check for meeting point
            if current_node.state in visited_other:
                return current_node.state

            for neighbor, direction, cost in self.maze.get_neighbors(current_node.state):
                if neighbor not in visited_this:
                    frontier.append(node.Node(neighbor, current_node))
            return None

        
        meet = expand_frontier(self.frontier_start, self.visited_start, self.visited_goal)
        if meet is None:
            meet = expand_frontier(self.frontier_goal, self.visited_goal, self.visited_start)

        
        if meet:
            self.running = False
            self.found_path = True
            self.reconstruct_bidirectional_path(meet)
    
    def reconstruct_bidirectional_path(self, meet_state):
        path_start = []
        node_start = self.visited_start[meet_state]
        while node_start:
            path_start.append(node_start.state)
            node_start = node_start.parent
        path_start.reverse()

        path_goal = []
        node_goal = self.visited_goal[meet_state].parent 
        while node_goal:
            path_goal.append(node_goal.state)
            node_goal = node_goal.parent

        self.path = path_start + path_goal