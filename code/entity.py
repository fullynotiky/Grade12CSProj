from abc import ABC
from math import sin

import pygame as pg

from globals import *


class Entity(pg.sprite.Sprite, ABC):
    def __init__(self, groups):
        super().__init__(groups)

        self.direction = pg.Vector2()
        self.frameIndex = 0
        self.animationSpeed = 0.15

    def checkDeath(self, command):
        if self.health <= 0:
            command()

    def collision(self, direction):
        if direction == HORIZONTAL:
            for sprite in self.obstacles:

                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.rect.left

                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.rect.right

        elif direction == VERTICAL:
            for sprite in self.obstacles:

                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.rect.top

                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.rect.bottom

    def move(self, speed: int):
        if self.direction.magnitude(): self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision(HORIZONTAL)

        self.hitbox.y += self.direction.y * speed
        self.collision(VERTICAL)

        self.rect.center = self.hitbox.center

    @staticmethod
    def getFlickerValue():
        val = sin(pg.time.get_ticks())
        if val >= 0:
            return 255
        else:
            return 0
