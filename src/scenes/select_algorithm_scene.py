import scenes.background as bg
import utils.global_settings as glb







class select_algorithm_scene(bg.background):
    def __init__(self):
        super().__init__()
        self.set_background_color(glb.WHITE)
        self.draw_buttons()
        
    def draw_buttons(self):
        button_width = 300
        button_height = 50
        # 8 buttons for selecting algorithms
        rect1_place = (glb.DEFAULT_SIZE[0] // 2 - 400, glb.DEFAULT_SIZE[1] // 2 - 200, button_width, button_height)
        text1 = "DFS"
        rect2_place = (glb.DEFAULT_SIZE[0] // 2 - 400, glb.DEFAULT_SIZE[1] // 2 - 100, button_width, button_height)
        text2 = "BFS"
        rect3_place = (glb.DEFAULT_SIZE[0] // 2 - 400, glb.DEFAULT_SIZE[1] // 2 + 100, button_width, button_height)
        text3 = "A*"
        rect4_place = (glb.DEFAULT_SIZE[0] // 2 - 400, glb.DEFAULT_SIZE[1] // 2 + 200, button_width, button_height)
        text4 = "Beam Search"
        rect5_place = (glb.DEFAULT_SIZE[0] // 2 + 200, glb.DEFAULT_SIZE[1] // 2 - 200, button_width, button_height)
        text5 = 'IDDFS'
        rect6_place = (glb.DEFAULT_SIZE[0] // 2 + 200, glb.DEFAULT_SIZE[1] // 2 - 100, button_width, button_height)
        text6 = 'UCS'
        rect7_place = (glb.DEFAULT_SIZE[0] // 2 + 200, glb.DEFAULT_SIZE[1] // 2 + 100, button_width, button_height)
        text7 = 'Bi-Directional Search'
        rect8_place = (glb.DEFAULT_SIZE[0] // 2 + 200, glb.DEFAULT_SIZE[1] // 2 + 200, button_width, button_height)
        text8 = 'IDA*'
        
        rect9_place = (glb.DEFAULT_SIZE[0] - button_width, 0, button_width, button_height)
        text9 = "Back to Menu"

        rect1 = bg.pygame.Rect(rect1_place)
        rect2 = bg.pygame.Rect(rect2_place)
        rect3 = bg.pygame.Rect(rect3_place)
        rect4 = bg.pygame.Rect(rect4_place)
        rect5 = bg.pygame.Rect(rect5_place)
        rect6 = bg.pygame.Rect(rect6_place)
        rect7 = bg.pygame.Rect(rect7_place)
        rect8 = bg.pygame.Rect(rect8_place)
        rect9 = bg.pygame.Rect(rect9_place)


        self.buttons.append(rect1)
        self.buttons.append(rect2)
        self.buttons.append(rect3)
        self.buttons.append(rect4)
        self.buttons.append(rect5)
        self.buttons.append(rect6)
        self.buttons.append(rect7)
        self.buttons.append(rect8)
        self.buttons.append(rect9)

        self.buttons_text.append(text1)
        self.buttons_text.append(text2)
        self.buttons_text.append(text3)
        self.buttons_text.append(text4)
        self.buttons_text.append(text5)
        self.buttons_text.append(text6)
        self.buttons_text.append(text7)
        self.buttons_text.append(text8)
        self.buttons_text.append(text9)

    def click_buttons(self, events):
        for event in events: 
            if event.type == bg.pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button in self.buttons:
                    if button.collidepoint(mouse_pos):
                        if button is not self.buttons[8]:
                            if button is self.buttons[0]:
                                glb.selected_algorithm = 'DFS'
                            if button is self.buttons[1]:
                                glb.selected_algorithm = 'BFS'
                            if button is self.buttons[2]:
                                glb.selected_algorithm = 'A*'
                            if button is self.buttons[3]:
                                glb.selected_algorithm = 'Beam Search'
                            if button is self.buttons[4]:
                                glb.selected_algorithm = 'IDDFS'
                            if button is self.buttons[5]:
                                glb.selected_algorithm = 'UCS'
                            if button is self.buttons[6]:
                                glb.selected_algorithm = 'Bi-Directional Search'
                            if button is self.buttons[7]:
                                glb.selected_algorithm = 'IDA*'
                            return "algorithm_scene"    
                        else:
                            return "select_map_scene"
        return 'select_algorithm_scene'