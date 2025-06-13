from http.client import FOUND
from tkinter import CURRENT
from tracemalloc import start

selected_map = None
selected_algorithm = None       # Currently running or last-run algorithm
pending_algorithm = None        # Selected in dropdown but not started yet

DEFAULT_SIZE = (1200, 800)

# DEFINED COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 105, 180)

WALL_COLOR = (100, 255, 255)   # Wall color
START_COLOR = (0, 255, 100)    # Start point color
END_COLOR = (255, 0, 100)      # End point color
PATH_COLOR = (255, 255, 255)   # Path color
VISITED_COLOR = (255, 100, 100)  # Visited cell color
FOUND_COLOR = (200, 255, 150)  # Found path color
LINE_COLOR = (0, 100, 255)     # Line color for path visualization

# Selection State


# Supported Algorithms
ALGORITHMS = ["DFS", "BFS", "A*", "Beam Search", "IDDFS", "UCS", "Bi-Directional Search", "IDA*"]

# Map Settings
MAP_ROWS = 20
MAP_COLS = 40
CELL_SIZE = 30
CURRENT_MAP = None

def reset_map_data():
    """Reset the map data to a default state."""
    map_data = [['1' for _ in range(MAP_COLS)] for _ in range(MAP_ROWS)]
    map_data[0][0] = 'S'  # Set the start point
    map_data[-1][-1] = 'E'  # Set the end point
    return map_data

def randomize_map_data():
    """Randomize the map data with walls and paths."""
    import random
    map_data = reset_map_data()
    for y in range(MAP_ROWS):
        for x in range(MAP_COLS):
            map_data[y][x] = '0' if random.random() < 0.3 else '1'  # 30% chance of being a wall
    total_nodes = MAP_ROWS * MAP_COLS
    start_index = random.randint(0, total_nodes - 1)
    end_index = random.randint(0, total_nodes - 1)
    while end_index == start_index:
        end_index = random.randint(0, total_nodes - 1)
    start_x, start_y = divmod(start_index, MAP_COLS)
    end_x, end_y = divmod(end_index, MAP_COLS)
    print(f"Start: ({start_x}, {start_y}), End: ({end_x}, {end_y})")
    map_data[start_x][start_y] = 'S'  # Set the start point
    map_data[end_x][end_y] = 'E'  # Set the end point
    global CURRENT_MAP
    CURRENT_MAP = map_data

def is_valid_color(color):
    """Check if the provided color is a valid RGB tuple."""
    return isinstance(color, tuple) and len(color) == 3 and all(0 <= c <= 255 for c in color)

def lighten_color(color, factor=0.2):
    """Lighten a color by a given factor."""
    return tuple(min(int(c + c * factor), 255) for c in color)

def return_scene(scene_name):
    return scene_name

def choose_algorithm(algorithm_name):
    """Store algorithm selection without activating it yet."""
    global pending_algorithm
    if algorithm_name in ALGORITHMS:
        pending_algorithm = algorithm_name
        print(f"Pending algorithm set to: {pending_algorithm}")
    else:
        print(f"Algorithm '{algorithm_name}' is not available. Please choose from {ALGORITHMS}.")