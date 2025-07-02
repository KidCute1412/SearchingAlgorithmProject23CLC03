from pydoc import text
import scenes.background as bg
import utils.global_settings as glb
import utils.load_resources as load_res
import algorithms.Algorithms as algos
import algorithms.AStar as AStar
import algorithms.DFS as DFS
import algorithms.UCS as UCS
import algorithms.BFS as BFS
import algorithms.BS as BS
import algorithms.BDS as BDS
import algorithms.IDAstar as IDA
import algorithms.IDDFS as IDDFS
import utils.button as but
import utils.modal as modal
import time





class algorithm_scene(bg.background):
    def __init__(self):
        super().__init__()
        self.set_background_color(glb.WHITE)
        self.draw_buttons()
        self.add_function_to_button()
        self.background_image = None
        self.modal = modal.Modal("Search failed!")
        self.modal_shown = False  
        self.ignore_next_click = False
        self.last_algorithm_select_time = 0.0
        self.block_draw_delay = 0.5  # giây
        # for rendering the map
        self.cell_size = glb.CELL_SIZE
        #self.map_data = copy.deepcopy(load_res.get_map(glb.selected_map))  # Copy the map data to avoid modifying the original
        glb.CURRENT_MAP = glb.reset_map_data()
        self.map_data = glb.CURRENT_MAP
        self.colors = {
            '1': glb.PATH_COLOR,  # Path
            '2': glb.MEDIUM_COLOR,  # Custom color for '2'
            '3': glb.HARD_COLOR,  # Custom color for '3'
            '0': glb.WALL_COLOR,  # Wall
            'S': glb.START_COLOR,    # Start
            'E': glb.END_COLOR,  # End
         }   
        self.base_x = (glb.DEFAULT_SIZE[0] - len(self.map_data[0]) * self.cell_size) // 2
        self.base_y = (glb.DEFAULT_SIZE[1] - len(self.map_data) * self.cell_size)
        self.algorithm : algos.searching_algorithms = None
        self.set_algorithm()
        self.algorithm = None
        self.stop_algorithm = False
        self.previous_mouse_pos = None
        self.incrementer = 0
        
        self.prev_algorithm_name = None
        self.prev_visited_count = 0
        self.prev_elapsed_time = 0.0
        self.prev_cost = None
        self.prev_algo_done = False
        #TIME
        self.elapsed = 0.0
        self.paused_total_time = 0
        self.pause_time = None
        self.is_paused = False
        self.font = bg.pygame.font.Font(glb.font_path, 24)

        # Cache
        self.cost_value_display = {}  # Dictionary to hold cost text surfaces
        self.cost_original_cache = {}
        self.cost_cache = {}  # Cache for cost values to avoid redrawing them every time
    
    # UNCOMMENT THIS IF YOU WANT TO USE OTHER ALGORITHMS
    def set_algorithm(self):
        
        if glb.selected_algorithm == 'DFS':
            self.algorithm = DFS.DFS()
        elif glb.selected_algorithm == 'BFS':
            self.algorithm = BFS.BFS()
        elif glb.selected_algorithm == 'A*':
            self.algorithm = AStar.AStar()
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


    def load_cache_cost(self):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell in ['0','1', '2', '3']:
                    cost_value = int(cell)
                    text = bg.pygame.font.SysFont(None, 24).render(str(cost_value), True, glb.BLACK)
                    text_surface = bg.pygame.Surface(text.get_size(), bg.pygame.SRCALPHA)
                    text_surface.blit(text, (0, 0))
                    text_surface.set_alpha(100)
                    self.cost_cache[(x, y)] = cost_value
                    self.cost_original_cache[(x, y)] = cost_value
                    self.cost_value_display[(x, y)] = text_surface

    def update_cost_cache(self, x, y, cost_value):
        font = bg.pygame.font.SysFont(None, 24)

        if str(cost_value).isdigit():
            text = font.render(str(cost_value), True, glb.BLACK)
            text_surface = bg.pygame.Surface(text.get_size(), bg.pygame.SRCALPHA)
            text_surface.blit(text, (0, 0))
            text_surface.set_alpha(100)  # Set transparency to 100
            self.cost_cache[(x, y)] = cost_value
            self.cost_value_display[(x, y)] = text_surface

    def render_cost_value(self, screen):    
        # Draw the cost text if it exists in the cache
        if not self.cost_cache:
            self.load_cache_cost()
        for (x, y), text_surface in self.cost_value_display.items():
            if self.cost_cache.get((x, y)) == 0 or self.cost_cache.get((x, y)) == 1 or self.cost_cache.get((x, y)) is None:
                continue
            if (x, y) in self.cost_value_display and self.cost_value_display[(x, y)]:
                text_rect = text_surface.get_rect(center=(
                    self.base_x + x * self.cell_size + self.cell_size // 2,
                    self.base_y + y * self.cell_size + self.cell_size // 2  
                ))
                screen.blit(text_surface, text_rect)        

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
                # draw cost text
        # Draw the cost values on the map
        self.render_cost_value(screen)
             

    def draw_buttons(self):
    
        button1 = but.Button("Start",
                            position=(700, 126), 
                            size=(150, 52),
                            main_color=glb.MINT,
                            color_hovered=glb.lighten_color(glb.MINT),
                            color_border=glb.MINT,
                            color_hovered_border=glb.lighten_color(glb.MINT),
                            font_size=30,
                            corner_radius=22,
                            text_color=glb.DARK_GREEN)

        button2 = but.Button("Return",
                            position=(1027, 126), 
                            size=(137, 52),
                            main_color=glb.UBE,
                            color_hovered=glb.lighten_color(glb.UBE),
                            color_border=glb.UBE,
                            color_hovered_border=glb.lighten_color(glb.UBE),
                            font_size=30,
                            corner_radius=22,
                            text_color=glb.DARK_PURPLE)
        button3 = but.Button("Reset",
                            position=(870, 126), 
                            size=(137, 52),
                            main_color=glb.UBE,
                            color_hovered=glb.lighten_color(glb.UBE),
                            color_border=glb.UBE,
                            color_hovered_border=glb.lighten_color(glb.UBE),
                            font_size=30,
                            corner_radius=22,
                            text_color=glb.DARK_PURPLE)
        # button4 = but.Button("Narrow Map", (0, 50), (200, 50))
        # button5 = but.Button("Room Map", (200, 0), (200, 50))

        maps = but.DropDownMenu(main_text="Modes", 
                                options_text=glb.MAPS,
                                position=(20, 110),
                                size=(200, 60),
                                main_color=glb.YELLOW,
                                color_hovered=glb.lighten_color(glb.YELLOW, 0.3),
                                color_border=glb.YELLOW,
                                color_hovered_border=glb.lighten_color(glb.YELLOW, 0.3),
                                font_size=25,
                                corner_radius=10,
                                text_color=glb.DARK_BROWN,
                                alt="Select a mode"
                                )

        menu = but.DropDownMenu(
            main_text="Algorithms",
            options_text=glb.ALGORITHMS,
            position=(250, 110),
            size=(300, 60),
            main_color=glb.YELLOW,
            color_hovered=glb.lighten_color(glb.YELLOW, 0.3),
            color_border=glb.YELLOW,
            color_hovered_border=glb.lighten_color(glb.YELLOW, 0.3),
            font_size=25,
            corner_radius=10,
            text_color=glb.DARK_BROWN,
            alt="Select an algorithm"
        )

        self.buttons.append(button1)
        self.buttons.append(button2)
        self.buttons.append(menu)
        self.buttons.append(maps)
        self.buttons.append(button3)





    def render_metrics(self, screen):
     
        if self.font is None:
            self.font = bg.pygame.font.SysFont(None, 32)

        screen_width = glb.DEFAULT_SIZE[0]
        screen_height = glb.DEFAULT_SIZE[1]
        
        y_offset = screen_height // 7

        # Current algorithm stats
        if self.algorithm and self.algorithm.start_time is not None:
            
            if not self.is_paused and not self.algorithm.found_path and self.algorithm.running:
                self.elapsed += self.algorithm.delta_time
            self.incrementer = (self.incrementer + 1) % 12

            pause = [".", ".", ".", ".", "..", "..", "..", "..", "...", "...", "...", "...", ]


            text_visited = self.font.render(f"Visited Nodes: {self.algorithm.visited_count}", True, glb.BLACK)
            text_time = self.font.render(f"Elapsed Time: {self.elapsed:.2f} s", True, glb.BLACK)
            text_size = self.font.render(f"Max Size: {self.algorithm.max_size} nodes ", True, glb.BLACK)
            if self.is_paused:
                text_cost = self.font.render(f"Paused!", True, glb.BLACK)
            elif self.modal_shown:
                text_cost = self.font.render(f"Blocked!", True, glb.BLACK)
            elif self.algorithm.found_path is False:
                text_cost = self.font.render(f"Running{pause[self.incrementer]}", True, glb.BLACK)
            else:
                text_cost = self.font.render(f"Total Path Cost: {self.algorithm.total_cost}", True, glb.BLACK)
            screen.blit(text_visited, (300, 64))
            screen.blit(text_size, (300, 22))
            screen.blit(text_time, (14, 64))
            screen.blit(text_cost,(14, 22))

        # Previous algorithm stats
        if self.prev_algorithm_name and self.prev_visited_count is not 0:
            prev_y_offset = y_offset
            text_prev_name = self.font.render(f"Previous Algorithm: {self.prev_algorithm_name}", True, (120, 120, 120))
            text_prev_visited = self.font.render(f"Visited Nodes: {self.prev_visited_count}", True, (120, 120, 120))
            text_prev_time = self.font.render(f"Elapsed Time: {self.prev_elapsed_time:.2f} s", True, (120, 120, 120))
            text_prev_cost = self.font.render(f"Total Path Cost: {self.prev_cost}", True, (120, 120, 120))
            
            screen.blit(text_prev_name, (680, 22))
            screen.blit(text_prev_cost, (680, 57))
            screen.blit(text_prev_visited, (960, 92))
            screen.blit(text_prev_time, (680, 92))

    def start_algorithm(self):
        
        # Reset time states
        self.elapsed = 0.0
        self.paused_total_time = 0.0
        self.is_paused = False
        self.pause_time = None
        self.stop_algorithm = False
        # Reset modal
        self.modal.visible = False
        self.modal_shown = False
        # Reset the algorithm 
        self.algorithm = None
        self.prev_algo_done = False
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
        self.buttons[2].add_function_to_button(0, lambda: glb.choose_algorithm('DFS'))
        self.buttons[2].add_function_to_button(1, lambda: glb.choose_algorithm('BFS'))
        self.buttons[2].add_function_to_button(2, lambda: glb.choose_algorithm('A*'))
        self.buttons[2].add_function_to_button(3, lambda: glb.choose_algorithm('Beam Search'))
        self.buttons[2].add_function_to_button(4, lambda: glb.choose_algorithm('IDDFS'))
        self.buttons[2].add_function_to_button(5, lambda: glb.choose_algorithm('UCS'))
        self.buttons[2].add_function_to_button(6, lambda: glb.choose_algorithm('Bi-Directional Search'))
        self.buttons[2].add_function_to_button(7, lambda: glb.choose_algorithm('IDA*'))
        self.buttons[3].add_function_to_button(0, lambda: glb.custom_map_data())               # Randomize Map
        self.buttons[3].add_function_to_button(1, lambda: glb.generate_maze_prim())               # Narrow Map
        self.buttons[3].add_function_to_button(2, lambda: glb.generate_maze_recursive_division()) # Room Map
        self.buttons[4].call_back = lambda: glb.reset_map_data()
    def stop_algorithm_function(self):
        self.stop_algorithm = not self.stop_algorithm

    def step(self):
        if self.stop_algorithm:
            return
        if self.algorithm is None:
            return
        if self.algorithm.running:
            self.algorithm.step()
            self.algorithm.calc_delta_time()
        if self.algorithm.running == False and self.algorithm.found_path == False and self.modal_shown == False:
            self.modal.visible = True
            self.modal_shown = True
            
    def select_in_menu(self):
        for algorithm_button in self.buttons[2].options:
            if algorithm_button.is_called:
                # CHANGE BUTTON TEXT AND FUNCTION
                self.buttons[0].text = "Start"
                self.buttons[0].call_back = lambda: self.start_algorithm()

                if self.prev_algo_done:
    
                    self.prev_algorithm_name = glb.selected_algorithm  # Save BEFORE it changes
                    self.prev_visited_count = getattr(self.algorithm, 'visited_count', len(self.algorithm.visited_nodes))
                    self.prev_elapsed_time = self.elapsed
                    self.prev_cost = self.algorithm.total_cost

                # Reset TIME and other states    
                self.elapsed = 0.0    
                self.algorithm = None    
                self.prev_algo_done = False
                self.modal_shown = False 
                self.modal.visible = False
                # Set the new algorithm
                glb.pending_algorithm = algorithm_button.text
                algorithm_button.is_called = False
                self.ignore_next_click = True  
                self.last_algorithm_select_time = time.time()
                print(f"Pending algorithm selected: {glb.pending_algorithm}")
                break
    
    def handle_randomize(self):
        for idx, option in enumerate(self.buttons[3].options):
            if option.is_called:
                # Gọi hàm tương ứng với chỉ số
                if idx == 0:
                    glb.custom_map_data()
                elif idx == 1:
                    glb.generate_maze_prim()
                elif idx == 2:
                    glb.generate_maze_recursive_division()
                #reset map sau khi thay đổi
                self.map_data = glb.CURRENT_MAP
                self.base_x = (glb.DEFAULT_SIZE[0] - len(self.map_data[0]) * self.cell_size) // 2
                self.base_y = (glb.DEFAULT_SIZE[1] - len(self.map_data) * self.cell_size)
                self.previous_mouse_pos = None
                self.prev_algorithm_name = None
                self.prev_visited_count = None
                self.prev_elapsed_time = None
                # CHANGE BUTTON TEXT AND FUNCTION
                self.buttons[0].text = "Start"
                self.buttons[0].call_back = lambda: self.start_algorithm()
                # Reset time states
                self.elapsed = 0.0
                self.paused_total_time = 0.0
                self.is_paused = False
                self.pause_time = None
                self.stop_algorithm = False
                # Reset modal
                self.modal.visible = False
                self.modal_shown = False
                # Reset the algorithm
                self.algorithm = None
                self.prev_algo_done = False
                # Cache cost
                self.cost_original_cache.clear()
                self.cost_cache.clear()  # Clear the cache to redraw costs
                self.load_cache_cost()  # Reload the cache with the new map data

                option.is_called = False
                break
        if self.buttons[4].is_called:
            glb.reset_map_data()
            self.map_data = glb.CURRENT_MAP
            self.base_x = (glb.DEFAULT_SIZE[0] - len(self.map_data[0]) * self.cell_size) // 2
            self.base_y = (glb.DEFAULT_SIZE[1] - len(self.map_data) * self.cell_size)
            self.previous_mouse_pos = None
            self.prev_algorithm_name = None
            self.prev_visited_count = None
            self.prev_elapsed_time = None
            # CHANGE BUTTON TEXT AND FUNCTION
            self.buttons[0].text = "Start"
            self.buttons[0].call_back = lambda: self.start_algorithm()
            # Reset time states
            self.elapsed = 0.0
            self.paused_total_time = 0.0
            self.is_paused = False
            self.pause_time = None
            self.stop_algorithm = False
            # Reset modal
            self.modal.visible = False
            self.modal_shown = False
            # Reset the algorithm
            self.algorithm = None
            self.prev_algo_done = False
            # Cache cost
            self.cost_original_cache.clear()
            self.cost_cache.clear()  # Clear the cache to redraw costs
            self.load_cache_cost()  # Reload the cache with the new map data

            
            
    def handle_custom_block(self, events):
        current_time = time.time()
        menu_open = any(isinstance(btn, but.DropDownMenu) and btn.is_open for btn in self.buttons)
        block_input = current_time - self.last_algorithm_select_time < self.block_draw_delay
        
        for event in events:
            if self.ignore_next_click:
                self.ignore_next_click = False
                continue
            if menu_open or block_input:
                continue  
            if event.type == bg.pygame.MOUSEMOTION and event.buttons[0]:
                self.custom_block(event.pos)

            if event.type == bg.pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.custom_block(event.pos, force_draw=True) 
        #Cache cost
        
        

    def update(self, events):

        next_scene = super().update(events)        
        # MODAL HANDLING
        self.modal.handle_event(events)
        if self.modal.visible:
            mouse_pos = bg.pygame.mouse.get_pos()
            if self.modal.rect.collidepoint(mouse_pos):
                self.ignore_next_click = True  # Ignore clicks while modal is open
        
        if  self.buttons[4].is_called:
            self.buttons[3].prev_name_main_button = "Modes"

        #RANDOMIZE MAP
        self.handle_randomize()
        
        # CHANGE ALGORITHM
        self.select_in_menu()
           
        # CUSTOM BLOCK
        self.handle_custom_block(events)
        

        # PAUSE, CONTINUE, RESTART
        self.pause_continue_restart()

        if next_scene:
            return next_scene          
        return 'algorithm_scene'
    
    def pause_continue_restart(self):
        # Stop the algorithm if it is running
        if self.algorithm and self.algorithm.running:
            self.buttons[0].call_back = lambda: self.stop_algorithm_function()
            if self.stop_algorithm:
                if not self.is_paused:
                    self.buttons[0].text = "Continue"
                    self.pause_time = time.time()
                    
                    self.is_paused = True
                
            else:    
                self.buttons[0].text = "Stop"
                if self.is_paused and self.pause_time is not None:
                    self.paused_total_time = time.time() - self.pause_time
                    print(f"Paused for {time.time() - self.pause_time:.2f} seconds.")
                    print(f"Total paused time: {self.paused_total_time:.2f} seconds.")
                    self.algorithm.delta_time = max (0.0, self.algorithm.delta_time - self.paused_total_time)
                    self.is_paused = False
                    self.pause_time = None 
                
        if self.algorithm and (self.algorithm.path or self.modal.visible):
                self.buttons[0].text = "Restart"
                self.buttons[0].call_back = lambda: self.start_algorithm()     
                 

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


        if not force_draw and (prev_x, prev_y) == (x, y):
            return

        self.previous_mouse_pos = mouse_pos

        if 0 <= x < len(self.map_data[0]) and 0 <= y < len(self.map_data):
            if self.map_data[y][x] in ['1', '2', '3']:
                # If the cell is a path, change it to a wall
                self.map_data[y][x] = '0'
                self.update_cost_cache(x, y, 0)
            elif self.map_data[y][x] == '0':
                cost_value = self.cost_original_cache.get((x, y), 1)  # Default to 1 if not found
                if cost_value == 0: 
                    cost_value = 1
                self.map_data[y][x] = str(cost_value)  # Change the wall to a path with cost
                self.update_cost_cache(x, y, cost_value)  # Update the cost cache with the new value
 
            

            

           
        
        
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
            self.prev_algo_done = True
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
            #draw the modal
        self.render_cost_value(screen)  # Render cost values on the map    
        if self.modal.visible:
            self.modal.draw(screen)
        self.render_metrics(screen)           

    def clean_up(self):
        glb.selected_algorithm = None
        glb.pending_algorithm = None
        self.algorithm = None
