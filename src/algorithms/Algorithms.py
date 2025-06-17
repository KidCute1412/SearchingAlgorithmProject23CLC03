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
        self.path = []
        self.running = False
        self.found_path = False
        self.current_node = None
        self.start_time = None
        self.delta_time = None
        self.delay_time = None
        self.visited_count = 0
        self.cost_type = None
        self.cost_val = None
        self.font = bg.pygame.font.SysFont("Arial", 24)
   
    def start(self):
        self.running = True
        self.start_time = time.time()
        return None
    def calc_delta_time(self):
        current_time = time.time()
        self.delta_time = max(0.0, current_time - self.start_time - self.delay_time * 1.0 / 1000)
        self.start_time = current_time
        print(self.delta_time)
   
        
    def step(self):
        pass
    def reconstruct_path(self, current = None):
        while current:
            self.path.append(current.state)
            current = current.parent
        self.path.reverse()
