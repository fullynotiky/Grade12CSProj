import pygame as pg

from globals import *


class Tile(pg.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], groups, type, surf=pg.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)

        self.spriteType = type
        self.image = surf
        yOffset = HITBOX_OFFSET[self.spriteType]

        if type == 'object': self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else: self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0, yOffset)
