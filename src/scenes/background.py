from webbrowser import get
import pygame
import utils.global_settings as glb






# # Initialize Pygame ONLY ONCE
pygame.init()





current_scene = 'welcome_scene'
# List of available scenes
scenes = [
    "welcome_scene",
    "select_map_scene",
    "select_algorithm_scene",
    "algorithm_scene",
    "DFS_algorithm",
    "exit",
]
class background:
    def __init__(self):
        # control buttons
        self.buttons = []
        #control text in button
        self.buttons_text = []
        # current button
        self.current_button = None

        # for background
        self.background_image = None
        self.background_color = glb.BLACK
        self.default_size = glb.DEFAULT_SIZE
    
    # CHECK HOVER BUTTON
    def hover_button(self):
        # get mouse position 
        mouse_pos = pygame.mouse.get_pos()
        # check if mouse is hovering over any button
        for button in self.buttons:
            button : pygame.Rect
            if button.collidepoint(mouse_pos):
                return button
        return None    
    
    # SET BACKGROUND COLOR

    def set_background_color(self, color):
        if glb.is_valid_color(color):
            self.background_color = color
        else:
            print("Invalid color format. Please provide a tuple of RGB values.")

    # COMMON UPDATE METHOD
    def update(self):
        self.current_button = self.hover_button() 

    def draw_buttons(self):
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
        
        
        #buttons    
        for button in self.buttons:
            pygame.draw.rect(screen, glb.BLUE, button)

        # texts on buttons    
        for i, text in enumerate(self.buttons_text):
            font = pygame.font.Font(None, 36)
            text_surface = font.render(text, True, glb.WHITE)
            text_rect = text_surface.get_rect(center=self.buttons[i].center)
            screen.blit(text_surface, text_rect)  

        # current button (make it become hovered)      
        if self.current_button:
            pygame.draw.rect(screen, glb.RED, self.current_button, 3)
        self.render_algorithm(screen)    
