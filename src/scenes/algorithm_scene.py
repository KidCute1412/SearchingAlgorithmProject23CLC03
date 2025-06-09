import scenes.background as bg
import utils.global_settings as glb
import utils.load_resources as load_res
import algorithms.Algorithms as algos
import algorithms.DFS as DFS
import algorithms.BDS as BDS
import algorithms.Astar as Astar
import algorithms.BFS as BFS
import algorithms.Beam as BS
import algorithms.IDAstar as IDAstar

class algorithm_scene(bg.background):
    def __init__(self):
        super().__init__()
        self.set_background_color(glb.WHITE)
        self.draw_buttons()
        self.background_image = None

        # for rendering the map
        self.cell_size = 50
        self.colors = {}
        self.base_x = 0
        self.base_y = 0
        self.map_data = load_res.get_map(glb.selected_map)
        self.draw_map()
        self.algorithm : algos.searching_algorithms = None
        self.set_algorithm()
    
    def set_algorithm(self):
        if glb.selected_algorithm == 'DFS':
            self.algorithm = DFS.DFS()
        elif glb.selected_algorithm == 'BFS':
            self.algorithm = BFS.BFS()
        elif glb.selected_algorithm == 'A*':
            self.algorithm = Astar.AStar()
        elif glb.selected_algorithm == 'Beam Search':
            self.algorithm = BS.BS()
        # elif glb.selected_algorithm == 'IDDFS':
        #     self.algorithm = algos.IDDFS_algorithm(self.map_data)
        # elif glb.selected_algorithm == 'UCS':
        #     self.algorithm = algos.UCS_algorithm(self.map_data)
        elif glb.selected_algorithm == 'Bi-Directional Search':
            self.algorithm = BDS.BDS()
        elif glb.selected_algorithm == 'IDA*':
            self.algorithm = IDAstar.IDAStar() 

    def draw_map(self):
        if not self.map_data:
            print("Map data in empty !")
            return
        self.cell_size = 50
        self.colors = {
            '1': (255, 255, 255),  # Path
            '0': (100, 255, 255),  # Wall
            'S': (0, 255, 100),    # Start
            'E': (255, 0, 100),  # End
         }   
        self.base_x = (glb.DEFAULT_SIZE[0] - len(self.map_data[0]) * self.cell_size) // 2
        self.base_y = (glb.DEFAULT_SIZE[1] - len(self.map_data) * self.cell_size) // 2
        
    def render_map(self, screen):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                color = self.colors.get(cell, (0, 0, 0))
                rect = bg.pygame.Rect(
                    self.base_x + x * self.cell_size,
                    self.base_y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                # Draw the cell
                bg.pygame.draw.rect(screen, color, rect)
                # Draw the border
                bg.pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    def draw_buttons(self):
    # Create font object
        font = bg.pygame.font.SysFont(None, 30)  # Adjust font size as needed
        
        # Calculate text sizes
        text1 = "Start " + glb.selected_algorithm
        text2 = "Exit Game"
        
        # Render text surfaces to measure their sizes
        text1_surface = font.render(text1, True, (0, 0, 0))
        text2_surface = font.render(text2, True, (0, 0, 0))
        
        # Add padding to text dimensions (20 pixels on each side)
        button1_width = text1_surface.get_width() + 80
        button2_width = text2_surface.get_width() + 80
        button_height = 50  # Fixed height
        
        # Position buttons
        rect1_place = (glb.DEFAULT_SIZE[0] // 2 - button1_width // 2, 0, button1_width, button_height)
        rect2_place = (glb.DEFAULT_SIZE[0] - button2_width - 10, 0, button2_width, button_height)
        
        # Create rectangles
        rect1 = bg.pygame.Rect(rect1_place)
        rect2 = bg.pygame.Rect(rect2_place)
        
        # Store buttons and text
        self.buttons = [rect1, rect2]
        self.buttons_text = [text1, text2]

    def step(self):
        if self.algorithm.running:
            self.algorithm.step()

    def click_buttons(self, events):
        for event in events: 
            if event.type == bg.pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button in self.buttons:
                    if button.collidepoint(mouse_pos):
                        if button is self.buttons[0]:
                            print('Start algorithm')
                            self.algorithm.start()
                        if button is self.buttons[1]:
                            return 'select_algorithm_scene'
        return 'algorithm_scene'        
    
    def render_algorithm(self, screen):
    # Render start search visited nodes
        for state in self.algorithm.visited_start:
            bg.pygame.draw.rect(screen, (255, 150, 150),  # Light red
                                (self.base_x + state[1] * self.cell_size,
                                self.base_y + state[0] * self.cell_size,
                                self.cell_size, self.cell_size))
        
        # Render goal search visited nodes
        for state in self.algorithm.visited_goal:
            bg.pygame.draw.rect(screen, (150, 150, 255),  # Light blue
                                (self.base_x + state[1] * self.cell_size,
                                self.base_y + state[0] * self.cell_size,
                                self.cell_size, self.cell_size))
        
        # Render final path
        if self.algorithm.path:
            for state in self.algorithm.path:
                bg.pygame.draw.rect(screen, (100, 255, 100),  # Green
                                    (self.base_x + state[1] * self.cell_size,
                                    self.base_y + state[0] * self.cell_size,
                                    self.cell_size, self.cell_size))
                    