import scenes.background as bg
import utils.global_settings as glb
import utils.load_resources as load_res
import algorithms.Algorithms as algos
import algorithms.DFS as DFS
import algorithms.UCS as UCS
import algorithms.BFS as BFS
import algorithms.BS as BS
import algorithms.BDS as BDS
import algorithms.IDAstar as IDA
import algorithms.IDDFS as IDDFS
import utils.button as but
import time





class algorithm_scene(bg.background):
    def __init__(self):
        super().__init__()
        self.set_background_color(glb.WHITE)
        self.draw_buttons()
        self.add_function_to_button()
        self.background_image = None

        # for rendering the map
        self.cell_size = glb.CELL_SIZE
        #self.map_data = copy.deepcopy(load_res.get_map(glb.selected_map))  # Copy the map data to avoid modifying the original
        glb.CURRENT_MAP = glb.reset_map_data()
        self.map_data = glb.CURRENT_MAP
        self.colors = {
            '1': glb.PATH_COLOR,  # Path
            '0': glb.WALL_COLOR,  # Wall
            'S': glb.START_COLOR,    # Start
            'E': glb.END_COLOR,  # End
         }   
        self.base_x = (glb.DEFAULT_SIZE[0] - len(self.map_data[0]) * self.cell_size) // 2
        self.base_y = (glb.DEFAULT_SIZE[1] - len(self.map_data) * self.cell_size)
        self.algorithm : algos.searching_algorithms = None
        self.set_algorithm()
        self.algorithm = None
        self.previous_mouse_pos = None
        self.font = bg.pygame.font.SysFont("Arial", 24)
        self.prev_algorithm_name = None
        self.prev_visited_count = None
        self.prev_elapsed_time = None
    
    # UNCOMMENT THIS IF YOU WANT TO USE OTHER ALGORITHMS
    def set_algorithm(self):
        if hasattr(self, 'algorithm') and self.algorithm:
            self.prev_name = glb.selected_algorithm  # Save BEFORE it changes
            self.prev_time = self.algorithm.total_time()
            self.prev_visited = getattr(self.algorithm, 'visited_count', len(self.algorithm.visited_nodes))
        else:
            self.prev_name = None
            self.prev_time = None
            self.prev_visited = None
        if glb.selected_algorithm == 'DFS':
            self.algorithm = DFS.DFS()
        elif glb.selected_algorithm == 'BFS':
            self.algorithm = BFS.BFS()
        # elif glb.selected_algorithm == 'A*':
        #     self.algorithm = algos.AStar_algorithm(self.map_data)
        elif glb.selected_algorithm == 'Beam Search':
            self.algorithm = BS.BS()
        elif glb.selected_algorithm == 'IDDFS':
            self.algorithm = IDDFS.IDDFS()
        elif glb.selected_algorithm == 'UCS':
            self.algorithm = UCS.UCS()
        elif glb.selected_algorithm == 'Bi-Directional Search':
            self.algorithm = BDS.BDS()
        elif glb.selected_algorithm == 'IDA*':
            self.algorithm = IDA.IDAStar()  

    def render_metrics(self, screen):
        if self.font is None:
            self.font = bg.pygame.font.SysFont(None, 32)

        screen_width = glb.DEFAULT_SIZE[0]
        screen_height = glb.DEFAULT_SIZE[1]
        
        y_offset = screen_height // 6

        # Current algorithm stats
        if self.algorithm and self.algorithm.start_time is not None:
            
            if self.algorithm.end_time is not None:
                elapsed = self.algorithm.total_time()
            else:
                elapsed = time.time() - self.algorithm.start_time -self.algorithm.delay_time * self.algorithm.visited_count / 1000

            text_visited = self.font.render(f"Visited Nodes: {self.algorithm.visited_count}", True, glb.BLACK)
            text_time = self.font.render(f"Elapsed Time: {elapsed:.2f} s", True, glb.BLACK)

            screen.blit(text_visited, text_visited.get_rect(center=(screen_width // 2, y_offset + 25)))
            screen.blit(text_time, text_time.get_rect(center=(screen_width // 2, y_offset + 55)))

        # Previous algorithm stats
        if self.prev_algorithm_name and self.prev_visited_count is not 0:
            prev_y_offset = y_offset - 90
            text_prev_name = self.font.render(f"Previous: {self.prev_algorithm_name}", True, (120, 120, 120))
            text_prev_visited = self.font.render(f"Visited Nodes: {self.prev_visited_count}", True, (120, 120, 120))
            text_prev_time = self.font.render(f"Elapsed Time: {self.prev_elapsed_time:.2f} s", True, (120, 120, 120))

            screen.blit(text_prev_name, text_prev_name.get_rect(center=(screen_width // 2, prev_y_offset + 25)))
            screen.blit(text_prev_visited, text_prev_visited.get_rect(center=(screen_width // 2, prev_y_offset + 55)))
            screen.blit(text_prev_time, text_prev_time.get_rect(center=(screen_width // 2, prev_y_offset + 85)))




        
        
    def render_map(self, screen):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                color = self.colors.get(cell, glb.BLACK)
                rect = bg.pygame.Rect(
                    self.base_x + x * self.cell_size,
                    self.base_y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                # Draw the cell
                bg.pygame.draw.rect(screen, color, rect)
                # Draw the border
                bg.pygame.draw.rect(screen, glb.BLACK, rect, 1)

    def draw_buttons(self):
    
        button1 = but.Button("Start Algorithm", (glb.DEFAULT_SIZE[0] // 2 - 100, 0), (200, 50))
        button2 = but.Button("Exit", (glb.DEFAULT_SIZE[0] - 200, 0), (200, 50))
        button3 = but.Button("Randomize Map", (glb.DEFAULT_SIZE[0] // 2 + 200, 100), (250, 50))
        
        menu = but.DropDownMenu("Select Algorithm", glb.ALGORITHMS, (100, 100), (300, 50))
        self.buttons.append(button1)
        self.buttons.append(button2)
        self.buttons.append(button3)
        self.buttons.append(menu)
    def start_algorithm(self):
        if self.algorithm is not None:
            self.prev_algorithm_name = glb.selected_algorithm

            if self.algorithm.start_time is not None:
                self.prev_visited_count = getattr(self.algorithm, 'visited_count', len(self.algorithm.visited_nodes))
                self.prev_elapsed_time = (
                    self.algorithm.total_time()
                    if self.algorithm.end_time is not None
                    else time.time() - self.algorithm.start_time
                )
            else:
                # Prevent crash if algorithm was not started
                self.prev_visited_count = 0
                self.prev_elapsed_time = 0.0

        # Apply the pending selection now
        if glb.pending_algorithm:
            glb.selected_algorithm = glb.pending_algorithm
            self.set_algorithm()

        if self.algorithm is None:
            print("No algorithm selected.")
            return

        print(f"Starting {glb.selected_algorithm} algorithm.")
        self.algorithm.start()
    def add_function_to_button(self):
        self.buttons[0].call_back = lambda: self.start_algorithm()
        self.buttons[1].call_back = lambda: glb.return_scene('welcome_scene')
        self.buttons[2].call_back = lambda: glb.randomize_map_data()
        self.buttons[3].add_function_to_button(0, lambda: glb.choose_algorithm('DFS'))
        self.buttons[3].add_function_to_button(1, lambda: glb.choose_algorithm('BFS'))
        self.buttons[3].add_function_to_button(2, lambda: glb.choose_algorithm('A*'))
        self.buttons[3].add_function_to_button(3, lambda: glb.choose_algorithm('Beam Search'))
        self.buttons[3].add_function_to_button(4, lambda: glb.choose_algorithm('IDDFS'))
        self.buttons[3].add_function_to_button(5, lambda: glb.choose_algorithm('UCS'))
        self.buttons[3].add_function_to_button(6, lambda: glb.choose_algorithm('Bi-Directional Search'))
        self.buttons[3].add_function_to_button(7, lambda: glb.choose_algorithm('IDA*'))


    def step(self):
        if self.algorithm is None:
            return
        if self.algorithm.running:
            self.algorithm.step()
    def select_in_menu(self):
        for algorithm_button in self.buttons[3].options:
            if algorithm_button.is_called:
                glb.pending_algorithm = algorithm_button.text
                algorithm_button.is_called = False
                print(f"Pending algorithm selected: {glb.pending_algorithm}")
                break
          
    def update(self, events):
        next_scene = super().update(events)
        
        self.buttons: list[but.Button] = self.buttons
        if self.buttons[2].is_called: # reset the map (randomize)

            self.map_data = glb.CURRENT_MAP
            self.base_x = (glb.DEFAULT_SIZE[0] - len(self.map_data[0]) * self.cell_size) // 2
            self.base_y = (glb.DEFAULT_SIZE[1] - len(self.map_data) * self.cell_size)
            self.previous_mouse_pos = None
            self.prev_algorithm_name = None
            self.prev_visited_count = None
            self.prev_elapsed_time = None
            if self.algorithm:
                self.algorithm.update_map()
        self.select_in_menu()
           
        # CUSTOM BLOCK
        for event in events:
            if event.type == bg.pygame.MOUSEMOTION and event.buttons[0]:
                self.custom_block(event.pos)

            if event.type == bg.pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.custom_block(event.pos, force_draw=True) 
        
        if next_scene:
            return next_scene          
        return 'algorithm_scene'
    
    
    def custom_block(self, mouse_pos, force_draw=False):
        if self.previous_mouse_pos is None:
            self.previous_mouse_pos = mouse_pos

        if not (self.base_x <= mouse_pos[0] < self.base_x + len(self.map_data[0]) * self.cell_size and
            self.base_y <= mouse_pos[1] < self.base_y + len(self.map_data) * self.cell_size):
            return

        prev_x = (self.previous_mouse_pos[0] - self.base_x) // self.cell_size
        prev_y = (self.previous_mouse_pos[1] - self.base_y) // self.cell_size
        x = (mouse_pos[0] - self.base_x) // self.cell_size
        y = (mouse_pos[1] - self.base_y) // self.cell_size

        # Nếu không phải force và vẫn cùng ô thì bỏ qua
        if not force_draw and (prev_x, prev_y) == (x, y):
            return

        self.previous_mouse_pos = mouse_pos

        if 0 <= x < len(self.map_data[0]) and 0 <= y < len(self.map_data):
            if self.map_data[y][x] == '1':
                self.map_data[y][x] = '0'
            elif self.map_data[y][x] == '0':
                self.map_data[y][x] = '1'
            

           
        
        
    def render_algorithm(self, screen):
        if self.algorithm is None:
            return
        for state in self.algorithm.visited_nodes:
            if state == self.algorithm.start_node or state == self.algorithm.end_node:
                continue
            # Draw the visited state
            bg.pygame.draw.rect(screen, glb.VISITED_COLOR, (self.base_x + state[1] * self.cell_size,
                                                     self.base_y + state[0] * self.cell_size,
                                                     self.cell_size, self.cell_size))
            # Draw the border around the visited state
            bg.pygame.draw.rect(screen, glb.BLACK, (self.base_x + state[1] * self.cell_size,
                                                     self.base_y + state[0] * self.cell_size,
                                                     self.cell_size, self.cell_size), 1)
            
        if self.algorithm.path:
            for state in self.algorithm.path:
                if state == self.algorithm.start_node or state == self.algorithm.end_node:
                    continue
                # Draw the found path state    
                bg.pygame.draw.rect(screen, glb.FOUND_COLOR, (self.base_x + state[1] * self.cell_size,
                                                             self.base_y + state[0] * self.cell_size,
                                                             self.cell_size, self.cell_size))
                # Draw the border around the found path state
                bg.pygame.draw.rect(screen, glb.BLACK, (self.base_x + state[1] * self.cell_size,    
                                                         self.base_y + state[0] * self.cell_size,
                                                         self.cell_size, self.cell_size), 1)
               
                
            
            # DRAW THE PATH
            for state_index in range(len(self.algorithm.path) - 1):
                
                bg.pygame.draw.line(screen, glb.LINE_COLOR,
                                     (self.base_x + self.algorithm.path[state_index][1] * self.cell_size + self.cell_size // 2,
                                      self.base_y + self.algorithm.path[state_index][0] * self.cell_size + self.cell_size // 2),
                                     (self.base_x + self.algorithm.path[state_index + 1][1] * self.cell_size + self.cell_size // 2,
                                      self.base_y + self.algorithm.path[state_index + 1][0] * self.cell_size + self.cell_size // 2), 3)
        self.render_metrics(screen)   
                

    # def click_buttons(self, events):
    #     for event in events: 
    #         if event.type == bg.pygame.MOUSEBUTTONDOWN and event.button == 1:
    #             mouse_pos = event.pos
    #             for button in self.buttons:
    #                 if button.collidepoint(mouse_pos):
    #                     if button is self.buttons[0]:
    #                         print('Start algorithm')
    #                         self.algorithm.start()
    #                     if button is self.buttons[1]:
    #                         return 'select_algorithm_scene'
    #                     if button is self.buttons[2]:
    #                         print('Randomize map')
    #                         glb.CURRENT_MAP = glb.randomize_map_data()
    #                         self.map_data = glb.CURRENT_MAP
    #                         self.base_x = (glb.DEFAULT_SIZE[0] - len(self.map_data[0]) * self.cell_size) // 2
    #                         self.base_y = (glb.DEFAULT_SIZE[1] - len(self.map_data) * self.cell_size)
    #                         self.previous_mouse_pos = None
    #                         if self.algorithm:
    #                             self.algorithm.update_map()
    #         if event.type == bg.pygame.MOUSEMOTION and event.buttons[0]:
                
    #             self.custom_block(event.pos)            
    #     return 'algorithm_scene'        