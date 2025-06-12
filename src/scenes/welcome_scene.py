import scenes.background as bg
import utils.global_settings as glb
from utils.load_resources import get_image
import utils.button as but 
class welcome_scene(bg.background):
    def __init__(self):
        super().__init__()
        self.background_image = get_image('welcome_background')
        self.draw_buttons()
        self.add_function_to_button()


    def draw_buttons(self):
        button1 = but.Button("Start Game", (glb.DEFAULT_SIZE[0] // 2 - 100, glb.DEFAULT_SIZE[1] // 2 - 50), (200, 50))
        button2 = but.Button("Exit Game", (glb.DEFAULT_SIZE[0] // 2 - 100, glb.DEFAULT_SIZE[1] // 2 + 10), (200, 50))
        self.buttons.append(button1)
        self.buttons.append(button2)
    def add_function_to_button(self):
        self.buttons: list[but.Button]
        self.buttons[0].call_back = lambda: glb.return_scene('algorithm_scene')
        self.buttons[1].call_back = lambda: glb.return_scene('exit')
    def update(self, event):
        next_scene = super().update(event)
        if next_scene:
            return next_scene
        return 'welcome_scene'
 
