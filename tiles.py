import pygame as pg
from settings import *

class Tile(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y


class SandTile(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = pg.surface.Surface((TILESIZE, TILESIZE))
        self.image.fill(TERRAIN)
        self.rect = self.image.get_rect()

class WaterTile(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = pg.surface.Surface((TILESIZE, TILESIZE))
        self.image.fill(WATER)
        self.rect = self.image.get_rect()