import utils.button as button
import utils.global_settings as glb
import pygame

class Modal:
    def __init__(self, message, close_button=None):
        self.message = message
        self.width = 400
        self.height = 200
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect(center=(glb.DEFAULT_SIZE[0] // 2, glb.DEFAULT_SIZE[1] // 2))
        self.font = pygame.font.SysFont("Arial", 24)
        self.close_button = button.Button(
            text="X", 
            position=(self.width - 30, 10), 
            size=(25, 25),
            call_back=self.hide)  # call the reference value
        self.visible = False

    def hide(self):
        self.visible = False
    def draw(self, screen):
        if not self.visible:
            return
        
        self.surface.fill((138, 206, 0))
        pygame.draw.rect(self.surface, glb.BLACK, self.surface.get_rect(), 2)

        # Render message
        text = self.font.render(self.message, True, glb.BLACK)
        text_rect = text.get_rect(center=(self.width // 2, 60))
        self.surface.blit(text, text_rect)

        # Draw close_button
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
