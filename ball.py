"""
Sprites classes
"""

import math
import pygame as pg
import random
import numpy as np

from player import Player
from math import cos, sin, acos, atan, atan2, degrees, pi, radians, sqrt
from itertools import cycle
from settings import *
from utils import *
vec = pg.math.Vector2


class Ball(pg.sprite.Sprite):
    def __init__(self, game, r, pos, vel, acc, color, is_game_ball) -> None:
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
        pg.sprite.Sprite.__init__(self)
        self.game = game
        
        self.color = color
        self.r = r
        self.initial_settings = (pos, vel, acc)
        self.is_game_ball = is_game_ball

        self.set_state(self.initial_settings)     
        self.obstacles = self.game.obstacles   
        self.rect = pg.Rect(self.pos.x-r, self.pos.y-r, self.r*2, self.r*2)
        self.old_rect = self.rect.copy()

    def set_state(self, settings) -> None:
        """_summary_
        """
        settings = (vec(setting) for setting in self.initial_settings)
        self.pos, self.vel, self.acc = settings    
        
        if self.is_game_ball:
            self.drop()
                
    def update(self) -> None:
        """_summary_
        """        
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
        self.obstacles_collisions("horizontal")
        
        # Updating y pos
        self.pos.y += self.vel.y + 0.5*self.acc.y
        self.rect.centery = self.pos.y
        
        # Obstacles collisions (vertical)
        self.obstacles_collisions("vertical")  
        other_particles = [
            particle for particle in self.game.particles.sprites() if particle != self]
        
        for p in other_particles:
            if overlap(self, p):
                self.ball_collision(p)
                break
    
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
            
    def obstacles_collisions(self, orientation) -> None:
        """_summary_

        Args:
            orientation (_type_): _description_
            is_ball (bool): _description_
        """
        collisions_sprites = pg.sprite.spritecollide(self, self.obstacles, False)
        
        if collisions_sprites:
            for sprite in collisions_sprites:
                if orientation == 'horizontal':
                    # right
                    if (self.rect.right >= sprite.rect.left and 
                            self.old_rect.right - 1 <= sprite.old_rect.left):
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.centerx
                        self.vel.x *= -1
                    # left 
                    if (self.rect.left <= sprite.rect.right and 
                            self.old_rect.left + 1 >= sprite.old_rect.right):
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.centerx
                        self.vel.x *= -1
                elif orientation == 'vertical':
                    # bottom 
                    if (self.rect.bottom >= sprite.rect.top and 
                            self.old_rect.bottom - 1 <= sprite.old_rect.top):
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.centery
                        self.vel.y *=-1 if self.is_game_ball else 0
                    # top
                    if (self.rect.top <= sprite.rect.bottom and 
                            self.old_rect.top + 1 >= sprite.old_rect.bottom):
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.centery
                        self.vel.y *=-1 if self.is_game_ball else 0

    def ball_collision(self, other) -> None:
        """_summary_

        Args:
            other (_type_): _description_
        """
        angle = compute_contact_angle(self, other)
        
        # Computing new velocities
        self.vel.x = self.vel.magnitude() * cos(angle)
        self.vel.y = self.vel.magnitude() * -sin(angle)
        
        # Dealing with sticky collisions
        d = pg.math.Vector2.magnitude(other.pos - self.pos)
        
        disp = (d - self.r - other.r) * 0.5
        dx = other.pos.x - self.pos.x
        dy = other.pos.y - self.pos.y
        
        self.pos.x += disp*(dx/d)
        self.pos.y += disp*(dy/d)
                        
    def drop(self) -> None:
        """_summary_
        """
        # Random angle between -45 and 45
        angle = random.uniform(0, math.pi) 
        v = self.vel.magnitude()
        self.vel.x, self.vel.y = v*cos(angle), v*-sin(angle)

   
def main():
    pass

if __name__ == "__main__":
    main()




