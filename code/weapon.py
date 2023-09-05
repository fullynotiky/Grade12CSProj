import pygame as pg

from player import Player
from settings import *


class Weapon(pg.sprite.Sprite):
    def __init__(self, groups, player: Player):
        super().__init__(groups)

        self.spriteType = WEAPON
        direction = player.state.split('_')[0]
        path = f'graphics\\weapons\\{player.weapon}\\{direction}.png'

        self.image = pg.image.load(path).convert_alpha()

        if direction == RIGHT: self.rect = self.image.get_rect(midleft=player.rect.midright + pg.Vector2(0, 16))
        elif direction == LEFT: self.rect = self.image.get_rect(midright=player.rect.midleft + pg.Vector2(0, 16))
        elif direction == DOWN: self.rect = self.image.get_rect(midtop=player.rect.midbottom + pg.Vector2(-10, 0))
        else: self.rect = self.image.get_rect(midbottom=player.rect.midtop + pg.Vector2(-10, 0))


