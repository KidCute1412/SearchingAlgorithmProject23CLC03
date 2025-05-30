DEFAULT_SIZE = (1200, 800)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)



selected_map = None
selected_algorithm = None
# DFS, BFS, A*, Beam Search, IDDFS, UCS, Bi-Directional Search, IDA*

def is_valid_color(color):
    """Check if the provided color is a valid RGB tuple."""
    return isinstance(color, tuple) and len(color) == 3 and all(0 <= c <= 255 for c in color)