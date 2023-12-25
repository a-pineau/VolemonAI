"""
Sprites classes
"""

import math
import pygame as pg
import random
import numpy as np

from math import (cos, degrees, sin, tan, acos, 
                  atan, atan2, pi, radians, sqrt)
from itertools import cycle
from settings import *
vec = pg.math.Vector2

class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, color=None) -> None: 
        pg.sprite.Sprite.__init__(self)
        self.pos = vec(x, y)
        self.image = pg.Surface((w, h))
        
        if color is not None:
            self.image.fill(color)
            
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.old_rect = self.rect.copy()

def main():
    pass

if __name__ == "__main__":
    main()




