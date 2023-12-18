# Define a dict of colours in RGB format- str: tuple

COLOURS = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
    'purple': (255, 0, 255),
    'orange': (255, 165, 0),
    'pink': (255, 192, 203),
    'brown': (165, 42, 42),
    'black': (0, 0, 0),
    'grey': (128, 128, 128),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'lime': (0, 255, 0),
    'maroon': (128, 0, 0),
    'navy': (0, 0, 128),
    'olive': (128, 128, 0),
    'teal': (0, 128, 128),
}


# Define default starting positions for a 20x20 board to ensure no overlaps
START_POS_20 = {
    0: [0, 0],
    1: [5, 0],
    2: [10, 0],
    3: [15, 0],
    4: [0, 5],
    5: [5, 5],
    6: [10, 5],
    7: [15, 5],
    8: [0, 10],
    9: [5, 10],
    10: [10, 10],
    11: [15, 10],
    12: [0, 15],
    13: [5, 15],
    14: [10, 15],
    15: [15, 15]
}