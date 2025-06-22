from http.client import FOUND
from math import e
from tkinter import CURRENT
from tracemalloc import start

selected_map = None
selected_algorithm = None       # Currently running or last-run algorithm
pending_algorithm = None        # Selected in dropdown but not started yet

DEFAULT_SIZE = (1200, 800)
font_path = "assets/fonts/SpaceGrotesk.ttf"
# DEFINED COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 105, 180)

DARK_BROWN = (50, 36, 0)
MINT = (102, 233, 168)
YELLOW = (250, 213, 113)
UBE = (249, 198, 247)
DARK_PURPLE = (76, 11, 74)
DARK_GREEN = (0, 47, 24)


WALL_COLOR = (100, 255, 255)   # Wall color
START_COLOR = (102, 233, 168)    # Start point color
END_COLOR = (203, 168, 214)      # End point color
PATH_COLOR = (255, 255, 255)   # Path color
VISITED_COLOR = (255, 100, 100)  # Visited cell color
FOUND_COLOR = YELLOW # Found path color
LINE_COLOR = (0, 100, 255)     # Line color for path visualization

# Supported Algorithms
ALGORITHMS = ["DFS", "BFS", "A*", "Beam Search", "IDDFS", "UCS", "Bi-Directional Search", "IDA*"]

#Modes
MAPS = ["Randomize", "Narrow", "Room"]

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
            random_value = random.random()
            if random_value < 0.3:
                map_data[y][x] = '0'  # 30% chance of being a wall
            elif random_value < 0.8:
                map_data[y][x] = '1'
            elif random_value < 0.9:
                map_data[y][x] = '2'
            else:
                map_data[y][x] = '3'        
    
            #map_data[y][x] = '0' if random.random() < 0.3 else '1'  # 30% chance of being a wall
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

def generate_maze_prim():
    import random

    map_data = [['0' for _ in range(MAP_COLS)] for _ in range(MAP_ROWS)]

    def in_bounds(x, y):
        return 0 <= x < MAP_COLS and 0 <= y < MAP_ROWS

    def get_neighbors(x, y):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and map_data[ny][nx] == '0':
                neighbors.append((nx, ny))
        return neighbors

    # Start from a random cell with odd coordinates
    start_x = random.randrange(1, MAP_COLS, 2)
    start_y = random.randrange(1, MAP_ROWS, 2)
    map_data[start_y][start_x] = '1'

    walls = []
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        nx, ny = start_x + dx, start_y + dy
        if in_bounds(nx, ny):
            walls.append(((start_x, start_y), (nx, ny)))

    while walls:
        (x1, y1), (x2, y2) = walls.pop(random.randint(0, len(walls) - 1))
        if map_data[y2][x2] == '0':
            wall_x = (x1 + x2) // 2
            wall_y = (y1 + y2) // 2
            ramdom_value = random.random()
            if ramdom_value < 0.5:
                map_data[wall_y][wall_x] = '1'
            elif ramdom_value < 0.8:
                map_data[wall_y][wall_x] = '2'
            else:
                map_data[wall_y][wall_x] = '3'        
            map_data[y1][x1] = '1'  # Mark the first cell as part of the path
            map_data[y2][x2] = '1'

            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = x2 + dx, y2 + dy
                if in_bounds(nx, ny) and map_data[ny][nx] == '0':
                    walls.append(((x2, y2), (nx, ny)))

    # Pick random start and end points on path tiles
    path_cells = [(x, y) for y in range(MAP_ROWS) for x in range(MAP_COLS) if map_data[y][x] == '1']
    start_x, start_y = random.choice(path_cells)
    end_x, end_y = random.choice(path_cells)
    while (start_x, start_y) == (end_x, end_y):
        end_x, end_y = random.choice(path_cells)

    map_data[start_y][start_x] = 'S'
    map_data[end_y][end_x] = 'E'

    print(f"Start: ({start_y}, {start_x}), End: ({end_y}, {end_x})")

    global CURRENT_MAP
    CURRENT_MAP = map_data

def generate_maze_recursive_division():
    import random

    map_data = [['1' for _ in range(MAP_COLS)] for _ in range(MAP_ROWS)]

    def in_bounds(x, y):
        return 0 <= x < MAP_COLS and 0 <= y < MAP_ROWS

    def divide(x, y, width, height, orientation):
        if width < 3 or height < 3:
            return

        horizontal = orientation == 'H'

        # Choose where to place the wall
        wx = x + (0 if horizontal else random.randrange(0, width // 2) * 2 + 1)
        wy = y + (random.randrange(0, height // 2) * 2 + 1 if horizontal else 0)

        # Choose the hole position
        px = wx + (random.randrange(0, width // 2) * 2 if horizontal else 0)
        py = wy + (0 if horizontal else random.randrange(0, height // 2) * 2)

        # Direction to move when placing the wall
        dx = 1 if not horizontal else 0
        dy = 0 if not horizontal else 1

        length = width if horizontal else height

        for i in range(length):
            cx = wx + i * dx
            cy = wy + i * dy
            if (cx, cy) != (px, py) and in_bounds(cx, cy):
                map_data[cy][cx] = '0'

        # Recursively divide the subareas
        if horizontal:
            divide(x, y, width, wy - y, choose_orientation(width, wy - y))
            divide(x, wy + 1, width, y + height - wy - 1, choose_orientation(width, y + height - wy - 1))
        else:
            divide(x, y, wx - x, height, choose_orientation(wx - x, height))
            divide(wx + 1, y, x + width - wx - 1, height, choose_orientation(x + width - wx - 1, height))

    def choose_orientation(width, height):
        if width < height:
            return 'H'
        elif height < width:
            return 'V'
        else:
            return random.choice(['H', 'V'])

    # Create border walls
    for y in range(MAP_ROWS):
        for x in range(MAP_COLS):
            random_value = random.random()
            #map_data[y][x] = '0' if x == 0 or y == 0 or x == MAP_COLS - 1 or y == MAP_ROWS - 1 else '1'
            if x == 0 or y == 0 or x == MAP_COLS - 1 or y == MAP_ROWS - 1:
                map_data[y][x] = '0'
            else:
                if random_value < 0.7:
                    map_data[y][x] = '1'
                elif random_value < 0.9:
                    map_data[y][x] = '2'
                else: 
                    map_data[y][x] = '3'            


    divide(1, 1, MAP_COLS - 2, MAP_ROWS - 2, choose_orientation(MAP_COLS - 2, MAP_ROWS - 2))

    # Pick random start and end points on path tiles
    path_cells = [(x, y) for y in range(MAP_ROWS) for x in range(MAP_COLS) if map_data[y][x] == '1']
    start_x, start_y = random.choice(path_cells)
    end_x, end_y = random.choice(path_cells)
    while (start_x, start_y) == (end_x, end_y):
        end_x, end_y = random.choice(path_cells)

    map_data[start_y][start_x] = 'S'
    map_data[end_y][end_x] = 'E'

    print(f"Start: ({start_y}, {start_x}), End: ({end_y}, {end_x})")

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

def choose_map(map_name):
    global pending_map
    if map_name in MAPS:
        pending_map = map_name
        print(f"Pending map set to: {pending_map}")
    else:
        print(f"Map '{map_name}' is not available. Please choose from {MAPS}.")
