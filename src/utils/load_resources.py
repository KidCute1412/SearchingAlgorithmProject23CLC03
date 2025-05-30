import pygame
import utils.global_settings as glb
images = {}
map = {}
def load_images():
    global images
    #welcome_background
    welcome_background = pygame.image.load('assets/images/welcome_background.jpg')
    welcome_background = pygame.transform.scale(welcome_background, glb.DEFAULT_SIZE)


    images = {
        'welcome_background': welcome_background,
    }

def load_one_map(file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                return [list(line.strip()) for line in lines]
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return []  

def load_map():
    global map
    map['Map1'] = load_one_map('assets/maps/Map1.txt')

def get_image(name):
    """Retrieve an image by its name."""
    return images.get(name)    

def get_map(name):
    """Retrieve a map by its name."""
    return map.get(name, [])  # Return an empty list if the map is not found