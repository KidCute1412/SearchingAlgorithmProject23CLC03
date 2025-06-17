import utils.global_settings as glb
import utils.load_resources as load_res
import scenes.background as bg
import scenes.welcome_scene as welcome
import scenes.algorithm_scene as algorithm_scene


class Game:
    def __init__(self):
        load_res.load_images()
        load_res.load_map()
        self.screen = bg.pygame.display.set_mode(glb.DEFAULT_SIZE)
        self.caption = bg.pygame.display.set_caption("PATH IN MAZE")
        self.current_scene = welcome.welcome_scene()
        self.running = True
        self.clock = bg.pygame.time.Clock()
    
    
    def control_scene(self, next_scene):
        if bg.current_scene == next_scene:
            return
        
        if next_scene not in bg.scenes:
            print(f"Scene '{next_scene}' does not exist.")
            return
        self.current_scene.clean_up()
        
        
        if next_scene == 'welcome_scene':
            bg.current_scene = 'welcome_scene'
            self.current_scene = welcome.welcome_scene()
        if next_scene == 'algorithm_scene':
            bg.current_scene = 'algorithm_scene'
            self.current_scene = algorithm_scene.algorithm_scene()   
        if next_scene == 'exit':
            bg.pygame.quit()
    
    def update(self, events):
        next_scene = self.current_scene.update(events)
        self.control_scene(next_scene)
    
    
    def render(self):
        self.current_scene.draw(self.screen)
    
    
    def run(self):
        while self.running:
            events = bg.pygame.event.get()
            for event in events:
                if event.type == bg.pygame.QUIT:
                    self.running = False
    
            #update
            self.update(events)
            # render
            self.render()
            bg.pygame.display.flip()
            self.screen.fill(glb.BLACK)    
            self.clock.tick(60)

        bg.pygame.quit()        




if __name__ == "__main__":
    my_game = Game()
    my_game.run()
            
                    


