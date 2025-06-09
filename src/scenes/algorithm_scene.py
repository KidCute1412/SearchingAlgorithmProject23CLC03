import scenes.background as bg
import utils.global_settings as glb
import utils.load_resources as load_res
import algorithms.Algorithms as algos
import algorithms.DFS as DFS
import algorithms.UCS as USC






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
        # elif glb.selected_algorithm == 'BFS':
        #     self.algorithm = algos.BFS_algorithm(self.map_data)
        # elif glb.selected_algorithm == 'A*':
        #     self.algorithm = algos.AStar_algorithm(self.map_data)
        # elif glb.selected_algorithm == 'Beam Search':
        #     self.algorithm = algos.BeamSearch_algorithm(self.map_data)
        # elif glb.selected_algorithm == 'IDDFS':
        #     self.algorithm = algos.IDDFS_algorithm(self.map_data)
        elif glb.selected_algorithm == 'UCS':
            self.algorithm = USC.USC()
        # elif glb.selected_algorithm == 'Bi-Directional Search':
        #     self.algorithm = algos.BiDirectionalSearch_algorithm(self.map_data)
        # elif glb.selected_algorithm == 'IDA*':
        #     self.algorithm = algos.IDAStar_algorithm(self.map_data)  

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
        rect1_place = (glb.DEFAULT_SIZE[0] // 2 - 100, 0, 200, 50)
        text1 = "Start DFS"
        rect2_place = (glb.DEFAULT_SIZE[0] - 200, 0, 200, 50)
        text2 = "Exit Game"
        rect1 = bg.pygame.Rect(rect1_place)
        rect2 = bg.pygame.Rect(rect2_place)
        self.buttons.append(rect1)
        self.buttons.append(rect2)
        self.buttons_text.append(text1)
        self.buttons_text.append(text2)

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
        for state in self.algorithm.visited_nodes:
            bg.pygame.draw.rect(screen, (255, 100, 100), (self.base_x + state[1] * self.cell_size,
                                                     self.base_y + state[0] * self.cell_size,
                                                     self.cell_size, self.cell_size))
            
        if self.algorithm.path:
            for state in self.algorithm.path:
                bg.pygame.draw.rect(screen, (100, 255, 100), (self.base_x + state[1] * self.cell_size,
                                                         self.base_y + state[0] * self.cell_size,
                                                         self.cell_size, self.cell_size))
                    