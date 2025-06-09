import algorithms.Node as node
import algorithms.Maze as maze
import algorithms.Algorithms as algos
import scenes.background as bg

class BDS(algos.searching_algorithms):
    def __init__(self):
        super().__init__()
        self.visited_start = set()
        self.visited_goal = set()
        
    def start(self):
        super().start()
        self.queue_start = [node.Node(self.maze.initial_state())]
        self.queue_goal = [node.Node(self.maze.goal_state())]
        self.visited_start_dict = {self.maze.initial_state(): None}
        self.visited_goal_dict = {self.maze.goal_state(): None}
        self.visited_nodes = set()
        
    def step(self):
        if not self.running:
            return
            
        # Expand from start
        if self.queue_start:
            current_node = self.queue_start.pop(0)
            if current_node.state not in self.visited_start:
                self.visited_start.add(current_node.state)
                self.visited_nodes.add(current_node.state)
                bg.pygame.time.delay(50)
                
                if current_node.state in self.visited_goal:
                    self._handle_intersection(current_node.state)
                    return
                    
                for neighbor, direction, cost in self.maze.get_neighbors(current_node.state):
                    if neighbor not in self.visited_start:
                        new_node = node.Node(neighbor, current_node, direction, 
                                           current_node.path_cost + cost)
                        self.queue_start.append(new_node)
                        self.visited_start_dict[neighbor] = current_node
        
        # Expand from goal
        if self.queue_goal:
            current_node = self.queue_goal.pop(0)
            if current_node.state not in self.visited_goal:
                self.visited_goal.add(current_node.state)
                self.visited_nodes.add(current_node.state)
                bg.pygame.time.delay(50)
                
                if current_node.state in self.visited_start:
                    self._handle_intersection(current_node.state)
                    return
                    
                for neighbor, direction, cost in self.maze.get_neighbors(current_node.state):
                    if neighbor not in self.visited_goal:
                        new_node = node.Node(neighbor, current_node, direction, 
                                           current_node.path_cost + cost)
                        self.queue_goal.append(new_node)
                        self.visited_goal_dict[neighbor] = current_node
        
    def _handle_intersection(self, intersection_state):
        self.running = False
        self.found_path = True
        
        # Reconstruct path from start to intersection
        path_from_start = []
        current_state = intersection_state
        while current_state is not None:
            path_from_start.append(current_state)
            current_node = self.visited_start_dict.get(current_state)
            current_state = current_node.state if current_node else None
        path_from_start.reverse()
        
        # Reconstruct path from intersection to goal
        path_from_goal = []
        current_state = intersection_state
        current_node = self.visited_goal_dict.get(current_state)
        while current_node is not None:
            path_from_goal.append(current_node.state)
            current_node = self.visited_goal_dict.get(current_node.state)
        
        # Combine paths - include intersection point only once
        self.path = path_from_start + path_from_goal
        
        # Make sure intersection point is in the path
        if intersection_state not in self.path:
            self.path.append(intersection_state)
