import pygame as pg
from PIL import Image
import terrain
from settings import *
import tiles
import math
import random

pg.init()

class Game():
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.create_map()
        self.run()

    def create_map(self):
        print("Creating map...")
        (offx, offy) = (random.randint(0, 100000), random.randint(0, 100000))
        terrain.render((offx, offy))

    def draw_map(self):
        self.map = Image.open("map.png")
        self.map = self.map.resize((WIDTH, HEIGHT))
        self.map = self.map.convert("RGBA")
        self.map = pg.image.fromstring(self.map.tobytes(), self.map.size, self.map.mode)
        self.screen.blit(self.map, (0, 0))

    def get_events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                if event.key == pg.K_r:
                    # recreate a new map
                    self.create_map()
                    self.draw_map()

    def run(self):
        while True :
            self.get_events()
            self.draw_map()
            pg.display.flip()

g = Game()
