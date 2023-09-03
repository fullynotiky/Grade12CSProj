import pygame as pg

from player import Player
from settings import *


class CameraGroup(pg.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

        self.floorOffsetRect = None
        self.display = pg.display.get_surface()
        self.offset = pg.Vector2()

        self.floorSurf = pg.image.load('graphics\\tilemap\\ground.png').convert_alpha()
        self.floorRect = self.floorSurf.get_rect(topleft=(0, 0))

    @staticmethod
    def getOffset(player):
        x = player.rect.centerx - WIDTH // 2
        y = player.rect.centery - HEIGHT // 2

        return x, y

    def draw(self, player: Player, **kwargs):
        self.offset.x = player.rect.centerx - WIDTH // 2
        self.offset.y = player.rect.centery - HEIGHT // 2

        self.floorOffsetRect = self.floorRect.topleft - self.offset
        self.display.blit(self.floorSurf, self.floorOffsetRect)

        for sprite in sorted(self.sprites(), key=lambda currSprite: currSprite.rect.centery):
            offsetRect = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offsetRect)

    def updateEnemy(self, player):
        enemySprites = [sprite for sprite in self.sprites() if (hasattr(sprite, 'spriteType')
                                                                and sprite.spriteType == ENEMY)]
        for sprite in enemySprites:
            sprite.enemyUpdate()
