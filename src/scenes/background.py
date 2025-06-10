import pygame
import utils.global_settings as glb
import utils.button as but





# # Initialize Pygame ONLY ONCE
pygame.init()





current_scene = 'welcome_scene'
# List of available scenes
scenes = [
    "welcome_scene",
    "algorithm_scene",
    "exit",
]
class background:
    def __init__(self):
        # control buttons

        self.buttons: list[but.Button] = []  # List of buttons

        # for background
        self.background_image = None
        self.background_color = glb.BLACK
        self.default_size = glb.DEFAULT_SIZE
       
    
    # SET BACKGROUND COLOR

    def set_background_color(self, color):
        if glb.is_valid_color(color):
            self.background_color = color
        else:
            print("Invalid color format. Please provide a tuple of RGB values.")

    # COMMON UPDATE METHOD
    def update(self, events):
        return_scene = None
        for button in self.buttons:
            
            check = None
            check = button.handle_event(events)
            if check:
                return_scene = check
        self.step()    
        return return_scene

         
    
    def draw_buttons(self):
        pass
    def add_function_to_button(self):
        pass
    def click_buttons(self, events):
        pass
    def draw_map(self, screen):
        pass
    def load_map(self, file_path):
        pass
    def render_map(self, screen):
        pass
    def step(self):
        pass
    def render_algorithm(self, screen):
        pass
    

    # COMMON DRAW METHOD
    def draw(self, screen):
        
        # background
        if self.background_image:
            screen.blit(self.background_image, (0, 0)) # (0, 0) is the top-left corner
        else:
            screen.fill(self.background_color)


        # draw map
        self.render_map(screen)
        
        # BUTTONS
        for button in self.buttons:
            #button: but.Button
            button.draw(screen)
        self.render_algorithm(screen)     
