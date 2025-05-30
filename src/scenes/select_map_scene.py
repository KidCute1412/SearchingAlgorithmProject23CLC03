import scenes.background as bg
import utils.global_settings as glb







class select_map_scene(bg.background):
    def __init__(self):
        super().__init__()
        self.set_background_color(glb.WHITE)
        self.draw_buttons()
        
    def draw_buttons(self):
        # 4 buttons for selecting maps
        rect1_place = (glb.DEFAULT_SIZE[0] // 2 - 400, glb.DEFAULT_SIZE[1] // 2 - 100, 200, 50)
        text1 = "Map 1"
        rect2_place = (glb.DEFAULT_SIZE[0] // 2 - 400, glb.DEFAULT_SIZE[1] // 2 + 100, 200, 50)
        text2 = "Map 2"
        rect3_place = (glb.DEFAULT_SIZE[0] // 2 + 200, glb.DEFAULT_SIZE[1] // 2 - 100, 200, 50)
        text3 = "Map 3"
        rect4_place = (glb.DEFAULT_SIZE[0] // 2 + 200, glb.DEFAULT_SIZE[1] // 2 + 100, 200, 50)
        text4 = "Map 4"

        rect5_place = (glb.DEFAULT_SIZE[0] - 200, 0, 200, 50)
        text5 = "Back to Menu"
        rect1 = bg.pygame.Rect(rect1_place)
        rect2 = bg.pygame.Rect(rect2_place)
        rect3 = bg.pygame.Rect(rect3_place)
        rect4 = bg.pygame.Rect(rect4_place)
        rect5 = bg.pygame.Rect(rect5_place)
        self.buttons.append(rect1)
        self.buttons.append(rect2)
        self.buttons.append(rect3)
        self.buttons.append(rect4)
        self.buttons.append(rect5)

        self.buttons_text.append(text1)
        self.buttons_text.append(text2)
        self.buttons_text.append(text3)
        self.buttons_text.append(text4)
        self.buttons_text.append(text5)

    def click_buttons(self, events):
        for event in events: 
            if event.type == bg.pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button in self.buttons:
                    if button.collidepoint(mouse_pos):
                        if button is not self.buttons[4]:
                            if button is self.buttons[0]:
                                glb.selected_map = 'Map1'
                            if button is self.buttons[1]:
                                glb.selected_map = 'Map2'
                            if button is self.buttons[2]:
                                glb.selected_map = 'Map3'
                            if button is self.buttons[3]:
                                glb.selected_map = 'Map4'
                            print(f"Selected {glb.selected_map}")    
                            # Return to select_algorithm_scene
                            return 'select_algorithm_scene'
                        if button is self.buttons[4]:
                            print("Back to menu")
                            return 'welcome_scene'
        return 'select_map_scene'