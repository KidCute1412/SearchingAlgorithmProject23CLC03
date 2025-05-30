from json import load
import algorithms.Maze as maze
import algorithms.Node as node
import utils.global_settings as glb
import utils.load_resources as load_res





class searching_algorithms:
    def __init__(self):
        self.maze = maze.Maze(load_res.get_map(glb.selected_map))
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
    def start(self):
        self.running = True
    def step(self):
        pass
    def reconstruct_path(self, current = None):
        while current:
            self.path.append(current.state)
            current = current.parent
        self.path.reverse()