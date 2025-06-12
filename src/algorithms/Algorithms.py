from json import load
import algorithms.Maze as maze
import utils.global_settings as glb
import utils.load_resources as load_res
import scenes.background as bg
import time




class searching_algorithms:
    def __init__(self):
        self.maze = maze.Maze(glb.CURRENT_MAP)
        if not self.maze:
            raise ValueError("Maze data is empty. Please load a valid maze.")
        self.start_node = self.maze.start
        self.end_node = self.maze.end
        self.visited_nodes = set()
        self.stack = []
        self.path = []
        self.running = False
        self.found_path = False
        self.current_node = None
        self.start_time = None
        self.end_time = None
        self.visited_count = 0
        self.font = bg.pygame.font.SysFont("Arial", 24)
    def update_map(self):
        self.maze = maze.Maze(glb.CURRENT_MAP)
        if not self.maze:
            raise ValueError("Maze data is empty. Please load a valid maze.")
        self.start_node = self.maze.start
        self.end_node = self.maze.end
        self.visited_nodes.clear()
        self.stack.clear()
        self.path.clear()
        self.running = False
        self.found_path = False
        self.start_time = None
        self.end_time = None
        self.visited_count = 0  
    def start(self):
        self.running = True
        self.start_time = time.time()
        return None
    def stop_timer(self):
        if self.start_time is not None:
            self.end_time = time.time()
    def total_time(self):
        if self.start_time is not None and self.end_time is not None:
            return self.end_time - self.start_time
        return None
    def step(self):
        pass
    def reconstruct_path(self, current = None):
        while current:
            self.path.append(current.state)
            current = current.parent
        self.path.reverse()