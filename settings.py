import os
import pygame as pg

vec = pg.math.Vector2

# Main window 
TITLE = "VolemonAI"
WIDTH = 1200
HEIGHT = 600
FPS = 60

# Directories
FILE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(FILE_DIR, "../imgs")
SNAP_FOLDER = os.path.join(FILE_DIR, "../snapshots")

# IDK
JUMP_SPEED = 7
JUMP_TOLERANCE = 1 
GRAVITY = 0.3

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)
DARK_TURQUOISE = (0, 206, 209)
LIGHT_SEA_GREEN = (32, 178, 170)

BACKGROUND = (30, 30, 30)

PARTICLES = {
    'agent':
        (
            45, 
            (WIDTH*0.75, HEIGHT-45), 
            vec(0, 0), vec(0, GRAVITY), 
            LIGHT_SEA_GREEN, False, 
        ),
    'game_ball':
        (
            45, 
            (WIDTH*0.75, HEIGHT*0.1),
            (2, 2), 
            (0, GRAVITY), 
            YELLOW, True,
        ) 
}

OBSTACLES = {
    'net':
        (
            WIDTH*0.5, HEIGHT-200*0.5,
            20, 200,
            WHITE 
        ),
    'bottom':
        (
            WIDTH*0.5, HEIGHT, 
            WIDTH, 1   
        ),
    'top':
        (
            WIDTH*0.5, 1, 
            WIDTH-1, 1
        ),
    'left':
        (
            -1, HEIGHT*0.5, 
            1, HEIGHT
        ),
    'right':
        (
            WIDTH, HEIGHT*0.5, 
            1, HEIGHT
        )
}


# MESSAGES
# Start round
START_ROUND_MSG = "Hit the spacebar to start"
START_ROUND_FONT_SIZE = 35
START_ROUND_COLOR = WHITE
START_ROUND_POSITION = WIDTH * 0.5, HEIGHT * 0.5
START_ROUND_SETTINGS = [
    START_ROUND_MSG,
    START_ROUND_FONT_SIZE,
    START_ROUND_COLOR,
    START_ROUND_POSITION
]




