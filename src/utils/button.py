import utils.global_settings as glb
import scenes.background as bg








class Button:
    def __init__(self, text, position, size, main_color = None, color_hovered = None, color_border = None, 
                 color_hovered_border = None,  font_size = 30, font_name = None, call_back = None, 
                 corner_radius = 30, text_color = glb.WHITE):
        self.text = text
        self.position = position
        self.size = size
        self.main_color = main_color
        self.main_color = main_color if main_color else glb.PINK
        self.color_hovered = color_hovered if color_hovered else glb.lighten_color(self.main_color, 0.5)
        self.color_border = color_border if color_border else glb.GREEN
        self.color_hovered_border = color_hovered_border if color_hovered_border else glb.RED
        self.text_color = text_color if text_color else glb.WHITE
        self.corner_radius = corner_radius
        self.font_size = font_size
        self.font_name = font_name if font_name else "Space Grotesk"
        self.call_back = call_back
        self.rect = bg.pygame.Rect(position, size)
        self.font = bg.pygame.font.Font(glb.font_path, self.font_size)
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.hovered = False
        self.is_called =False

    def draw(self, screen):
        # Draw the button rectangle
        bg.pygame.draw.rect(screen, self.main_color, self.rect, border_radius=self.corner_radius)
        bg.pygame.draw.rect(screen, self.color_border, self.rect, 2, border_radius=self.corner_radius)
        # Draw the text on the button
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, self.text_rect) 
        if self.hovered:
            # Draw the hovered state
            bg.pygame.draw.rect(screen, self.color_hovered, self.rect, border_radius=self.corner_radius)
            # Draw the hovered border
            bg.pygame.draw.rect(screen, self.color_hovered_border, self.rect, 2, border_radius=self.corner_radius)
            screen.blit(self.text_surface, self.text_rect)

    def handle_event(self, events):
        return_value = None
        self.is_called = False
        for event in events:
            if event.type == bg.pygame.MOUSEMOTION:
                mouse_pos = event.pos
                self.hovered = self.rect.collidepoint(mouse_pos)
            if event.type == bg.pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered:
                # Function of the button is called
                    return_value = self.call_back()
                    print(f"Button '{self.text}' clicked.")
                    self.is_called = True    
        return return_value        

              

        
class DropDownMenu:
    def __init__(self, main_text, options_text, position, size,
                 main_color, color_hovered, color_border, 
                 color_hovered_border, font_size=30, font_name=None, 
                 corner_radius=0, text_color=glb.WHITE,
                 alt=""):
        self.main_button = Button(text = main_text,
                                 position= position,
                                 size=size,
                                call_back = self.toggle,
                                main_color=main_color,
                                color_hovered=color_hovered,
                                color_border=color_border,
                                color_hovered_border=color_hovered_border,
                                font_size=font_size,
                                font_name=font_name,
                                corner_radius=corner_radius,
                                text_color=text_color)
        self.options = [Button(text, (position[0], position[1] + (i + 1)* size[1]), size,
                        main_color=main_color,
                        color_hovered=color_hovered,
                        color_border=color_border,
                        color_hovered_border=color_hovered_border,
                        font_size=font_size,
                        font_name=font_name,
                        corner_radius=corner_radius,
                        text_color=text_color)
                        for i, text in enumerate(options_text)]
        self.is_open = False
        self.prev_name_main_button = None
        self.alt = alt

    def toggle(self):
        self.is_open = not self.is_open    
        return None
        
    def add_function_to_button(self, index, call_back):
        if 0 <= index < len(self.options):
            self.options[index].call_back = call_back
        else:
            print(f"Index {index} is out of range for options.") 

    def draw(self, screen):
        self.main_button.draw(screen)
        if self.is_open:
            for option in self.options:
                option.draw(screen)
    def change_main_text(self, new_text):
        self.main_button.text = new_text
        self.main_button.text_surface = self.main_button.font.render(new_text, True, glb.WHITE)
        self.main_button.text_rect = self.main_button.text_surface.get_rect(center=self.main_button.rect.center)
        
    def handle_event(self, events):
        return_value = None
        for event in events:
            if event.type == bg.pygame.MOUSEBUTTONDOWN and event.button == 1:
                # click outside the down menu to close it
                if not self.main_button.rect.collidepoint(event.pos) and \
                all(not opt.rect.collidepoint(event.pos) for opt in self.options):
                    self.is_open = False
        self.main_button.handle_event(events)
        if self.is_open:
            self.change_main_text(self.alt)
            for option in self.options:
                option.handle_event(events)
                if option.is_called:
                    self.change_main_text(option.text)
                    self.prev_name_main_button = option.text
                    self.is_open = False
                    for opt in self.options:
                        opt: Button
                        opt.hovered = False
                    break
        else:
            if self.prev_name_main_button:
                self.change_main_text(self.prev_name_main_button)        
        
                

        
        return return_value    
    
    
    def is_opened(self):
        return self.is_open                     
        

  