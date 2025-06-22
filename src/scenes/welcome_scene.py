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
        button1 = but.Button(
            text="Start",
            position=(374, 489),
            size=(190, 72),
            main_color=glb.MINT,
            color_hovered=glb.lighten_color(glb.MINT),
            color_border=glb.MINT,
            color_hovered_border=glb.lighten_color(glb.MINT),
            font_size=42,
            corner_radius=30,
            text_color=glb.DARK_GREEN
        )

        button2 = but.Button(
            text="Exit",
            position=(635, 489),
            size=(190, 72),
            main_color=glb.YELLOW,
            color_hovered=glb.lighten_color(glb.YELLOW),
            color_border=glb.YELLOW,
            color_hovered_border=glb.lighten_color(glb.YELLOW),
            font_size=42,
            corner_radius=30,
            text_color=glb.DARK_BROWN
        )        
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
 
