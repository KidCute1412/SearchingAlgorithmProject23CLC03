import scenes.background as bg
import utils.global_settings as glb
from utils.load_resources import get_image
class welcome_scene(bg.background):
    def __init__(self):
        super().__init__()
        self.background_image = get_image('welcome_background')
        self.draw_buttons()


    def draw_buttons(self):
        rect1_place = (glb.DEFAULT_SIZE[0] // 2 - 100, glb.DEFAULT_SIZE[1] // 2 - 50, 200, 50)
        text1 = "Start Game"
        rect2_place = (glb.DEFAULT_SIZE[0] // 2 - 100, glb.DEFAULT_SIZE[1] // 2 + 10, 200, 50)
        text2 = "Exit Game"
        rect1 = bg.pygame.Rect(rect1_place)
        rect2 = bg.pygame.Rect(rect2_place)
        self.buttons.append(rect1)
        self.buttons.append(rect2)
        self.buttons_text.append(text1)
        self.buttons_text.append(text2)

    def click_buttons(self, events):
        for event in events: 
            if event.type == bg.pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button in self.buttons:
                    
                    if button.collidepoint (mouse_pos):
                        if button is self.buttons[0]:
                            return 'select_map_scene'
                        if button is self.buttons[1]:
                            return 'exit'
        return 'welcome_scene'    
