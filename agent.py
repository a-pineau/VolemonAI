"""
Sprites classes
"""

import math
import pygame as pg
import random
import numpy as np

from ball import Ball
from math import cos, sin, acos, atan, atan2, degrees, pi, radians, sqrt
from settings import *
from utils import *
vec = pg.math.Vector2


class Agent(Ball):
    def __init__(self) -> None:
        """_summary_

        Args:
            game (_type_): _description_
            r (_type_): _description_
            x (_type_): _description_
            y (_type_): _description_
            vel (_type_): _description_
            acc (_type_): _description_
            color (_type_): _description_
        """
        super().__init__(self)

        
    def update(self) -> None:
        """_summary_
        """
        
        is_ball = (self == self.game.ball)
        
        # Rect at previous frame
        # self.old_rect = self.rect.copy()
        # if self == self.game.player: # Player only
        #     self.vel.x = 0
        #     keys = pg.key.get_pressed() # Keyboard events
            
        #     if keys[pg.K_RIGHT]:
        #         self.vel.x += PLAYER_X_SPEED
        #     elif keys[pg.K_LEFT]:
        #         self.vel.x += -PLAYER_X_SPEED
                
        # Updating velocity (the horizontal component remains the same)
        self.vel.y += self.acc.y
        
        # Updating x pos
        self.pos.x += self.vel.x
        self.rect.centerx = self.pos.x
        
        # Obstacles collisions (horizontal)
        self.obstacles_collisions("horizontal", is_ball)
        
        # Updating y pos
        self.pos.y += self.vel.y + 0.5*self.acc.y
        self.rect.centery = self.pos.y
        
        # Obstacles collisions (vertical)
        self.obstacles_collisions("vertical", is_ball)  
             
        # Ball collision (on floor)
        if not is_ball and self.is_standing([self.game.bottom]):
            self.on_floor_ball_collision()
        else:
            particles = self.game.balls.sprites()
            
            for i, p in enumerate(particles):
                for other in particles[i+1:]:
                    p.on_air_ball_collision(other)

    def overlap(self, other) -> bool:
        """_summary_

        Args:
            other (_type_): _description_

        Returns:
            bool: _description_
        """
        return self.pos.distance_to(other.pos) < self.r + other.r
    
    def is_standing(self, obstacles, tolerance=1) -> bool:
        """_summary_

        Args:
            obstacles (_type_): _description_
            tolerance (int, optional): _description_. Defaults to 1.

        Returns:
            bool: _description_
        """
        standing = False
        self.rect.bottom += tolerance
        
        sprites = pg.sprite.Group()
        sprites.add(*obstacles)
        
        # Checking for collisions with the given obstacles
        collisions_sprites = pg.sprite.spritecollide(self, obstacles, False)
        if collisions_sprites:
            for sprite in collisions_sprites:
                if self.rect.bottom >= sprite.rect.top:
                    standing = True
                    break
                
        self.rect.bottom -= tolerance
        return standing
 
    def jump(self) -> None:  
        """_summary_
        """
        if self.is_standing([self.game.bottom, self.game.net], PLAYER_JUMP_TOLERANCE): 
            self.vel.y = -PLAYER_Y_SPEED
            
    def obstacles_collisions(self, orientation, is_ball) -> None:
        """_summary_

        Args:
            orientation (_type_): _description_
            is_ball (bool): _description_
        """
        collisions_sprites = pg.sprite.spritecollide(self, self.obstacles, False)
        
        if collisions_sprites:
            for sprite in collisions_sprites:
                if orientation == 'horizontal':
                    # Right
                    if (self.rect.right >= sprite.rect.left and 
                            self.old_rect.right - 1 <= sprite.old_rect.left):
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.centerx
                        self.vel.x *= -1
                    # Left 
                    if (self.rect.left <= sprite.rect.right and 
                            self.old_rect.left + 1 >= sprite.old_rect.right):
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.centerx
                        self.vel.x *= -1
                elif orientation == 'vertical':
                    # Bottom 
                    if (self.rect.bottom >= sprite.rect.top and 
                            self.old_rect.bottom - 1 <= sprite.old_rect.top):
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.centery
                        self.vel.y *= -1
                    # Top
                    if (self.rect.top <= sprite.rect.bottom and 
                            self.old_rect.top + 1 >= sprite.old_rect.bottom):
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.centery
                        self.vel.y *= -1
                        
    def drop(self) -> None:
        """_summary_
        """
        # Random angle between -45 and 45
        angle = random.uniform(-math.pi/4, math.pi/4) 
        print(angle)
        v = self.vel.magnitude()
        self.vel.x, self.vel.y = v*cos(angle), v*-sin(angle)
   
    def predict_range(self, angle) -> int:
        """_summary_

        Args:
            angle (_type_): _description_
            g (_type_, optional): _description_. Defaults to BALL_GRAVITY.

        Returns:
            int: _description_
        """
        x0, y0 = self.pos.x, y0 = HEIGHT - self.pos.y - self.r
        v = self.vel.magnitude()
        
        r = v*cos(angle) 
        r *= v*sin(angle) + sqrt((v*sin(angle))**2 + 2*BALL_GRAVITY*y0)
        r /= BALL_GRAVITY
        r += x0
        
        return int(r)
   
def main():
    pass

if __name__ == "__main__":
    main()




