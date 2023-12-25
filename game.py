"""Implements the game loop and handles the user's events."""

import os
import time
import pygame as pg

from itertools import cycle
from player import Player
from ball import Ball
from obstacle import Obstacle
from settings import *
from os.path import join, dirname, abspath

vec = pg.math.Vector2
n_snap = 0

# Manually places the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 50)

class Game:
    def __init__(self) -> None:
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.last_time = time.time()
        
        self.running = True  
        self.record = False
        self.start_round = False
        self.stop_timer = False
        self.anticipate = False
        
        self.n_frame = 0
        self.scores = {"Player": 0, "Bot": 0}
    
    def new(self) -> None:
        """_summary_
        """
        try:
            os.makedirs(SNAP_FOLDER)
        except FileExistsError:
            print(f"Folder \"{SNAP_FOLDER}\" already exists. Ignoring.")
        if os.path.isdir(SNAP_FOLDER):
            for file_name in os.listdir(SNAP_FOLDER):
                file = os.path.join(SNAP_FOLDER, file_name)
                os.remove(file)
                
        # Defining sprite groups
        self.particles = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        
        # Particles (balls)
        for particle_settings in PARTICLES.values():
            particle = Ball(self, *particle_settings)
            if particle.is_game_ball:
                self.game_ball = particle
            self.particles.add(particle)
        
        # Obstacles
        for obstacle_settings in OBSTACLES.values():
            obstacle = Obstacle(*obstacle_settings)
            self.obstacles.add(obstacle)
                    
    def delta_time(self):
        current_time = time.time()
        self.dt = current_time - self.last_time
        self.last_time = current_time
    
    def run(self):
        """_summary_
        """
        self.playing = True
        
        while self.playing: 
            self.n_frame += 1
            self.dt = self.clock.tick(FPS)*1e-3
            self.events()
            self.update() 
            self.display()
    
    def update(self) -> None:
        """_summary_

        Args:
            ball_init (_type_): _description_
        """
        self.particles.update()
        self.obstacles.update()
        
        if self.episode_over():
            for particle in self.particles:
                particle.set_state(particle.initial_settings)
                
    def episode_over(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return self.game_ball.rect.bottom >= HEIGHT
                    
    def events(self):
        """_summary_
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if self.start_round:
                        self.player.jump()
                    else:
                        self.start_round = True
                        self.timer = 0
                elif event.key == pg.K_q:
                    if self.playing:
                        self.playing = False
                    self.running = False

    def display(self):
        """
        TODO

        Parameters
        ----------

        Returns
        -------
        """
        self.screen.fill(BACKGROUND)
        
        for particle in self.particles.sprites():
            pg.draw.circle(self.screen, particle.color, particle.pos, particle.r)
            
        self.obstacles.draw(self.screen)
        pg.display.flip()  

    def record_game(self) -> None:
        """Save a snapshot of the current screen to the SNAP_FOLDER.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """

        global n_snap
        extension = "png"
        file_name = f"snapshot_{n_snap}.{extension}"
        pg.image.save(self.screen, os.path.join(SNAP_FOLDER, file_name))
        n_snap += 1
        
def main():
    game = Game()
    while game.running:
        game.new()
        game.run()
    pg.quit()

if __name__ == "__main__":
    main()