import utils.button as button
import utils.global_settings as glb
import scenes.background as bg
import pygame

class Modal:
    def __init__(self, message, close_button=None, color=glb.YELLOW):
        self.message = message
        self.width = 400
        self.height = 200
        self.color = color
        self.corner_radius = 20

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect(center=(glb.DEFAULT_SIZE[0] // 2, glb.DEFAULT_SIZE[1] // 2))
        self.font = pygame.font.Font(glb.font_path, 32)
        self.close_button = button.Button(
            text="Close", 
            position=(265, 132), 
            size=(128, 60),
            font_size=32,
            corner_radius=20,
            main_color=glb.UBE,
            color_hovered=glb.lighten_color(glb.UBE),
            color_border=glb.UBE,
            color_hovered_border=glb.lighten_color(glb.UBE),
            text_color=glb.DARK_PURPLE,
            call_back=self.hide)  # call the reference value
        self.visible = False
            # Tạo surface với alpha (để bo góc trong suốt)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(glb.DEFAULT_SIZE[0] // 2, glb.DEFAULT_SIZE[1] // 2))

    def hide(self):
        self.visible = False
    def draw(self, screen):
        if not self.visible:
            return
        
        self.surface.fill((0, 0, 0, 0))  # Transparent background
        pygame.draw.rect(self.surface, self.color, self.surface.get_rect(), border_radius=self.corner_radius)        # Render message
        text = self.font.render(self.message, True, glb.DARK_PURPLE)        
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 20))
        self.surface.blit(text, text_rect)
        self.close_button.draw(self.surface)
        screen.blit(self.surface, self.rect.topleft)
             
    def handle_event(self, events):
        if self.visible == False:
            return
        else:
            for event in events:
                if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
                    rel_pos = (event.pos[0] - self.rect.left, event.pos[1] - self.rect.top)
                    new_event = pygame.event.Event(event.type, {'pos': rel_pos, 'button': getattr(event, 'button', None)})
                    self.close_button.handle_event([new_event])
                else:
                    self.close_button.handle_event([event])
