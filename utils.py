"""
Sprites classes
"""

import math
import pygame as pg
import numpy as np

from player import Player

from itertools import cycle
from settings import *
vec = pg.math.Vector2


def compute_distance(p1, p2) -> float:
    """_summary_

    Args:
        p1 (_type_): _description_
        p2 (_type_): _description_

    Returns:
        float: _description_
    """
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def overlap(b1, b2) -> bool:
    """_summary_

    Args:
        other (_type_): _description_

    Returns:
        bool: _description_
    """
    return compute_distance(b1.pos, b2.pos) < b1.r + b2.r

def compute_contact_angle(b1, b2) -> float:
    """_summary_

    Args:
        object1_position (_type_): _description_
        object2_position (_type_): _description_

    Returns:
        float: _description_
    """
    dx, dy = b2.pos.x - b1.pos.x, b2.pos.y - b1.pos.y
    contact_angle = math.pi - math.atan2(dy, dx)
    return contact_angle

def predict_range(x0, y0, v, angle) -> int:
    """_summary_

    Args:
        x0 (_type_): _description_
        y0 (_type_): _description_
        v (_type_): _description_
        angle (_type_): _description_

    Returns:
        int: _description_
    """        
    r = v*math.cos(angle) 
    r *= v*math.sin(angle) + math.sqrt((v*math.sin(angle))**2 + 2*BALL_GRAVITY*y0)
    r /= BALL_GRAVITY
    r += x0
    
    return int(r)
   
   
def main():
    pass

if __name__ == "__main__":
    main()




