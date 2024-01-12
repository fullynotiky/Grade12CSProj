import pygame as pg

from abc import ABC
from math import sin
from globals import *


class Entity(pg.sprite.Sprite, ABC):
    def __init__(self, groups):
        super().__init__(groups)

        self.direction = pg.Vector2()
        self.frameIndex = 0
        self.animationSpeed = 0.15

    def checkDeath(self, command):
        if self.health <= 0: command()

    def collision(self, direction):
        if direction == HORIZONTAL:
            for sprite in self.obstacles:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0: self.hitbox.right = sprite.rect.left  # moving right
                    if self.direction.x < 0:  self.hitbox.left = sprite.rect.right  # moving left

        elif direction == VERTICAL:
            for sprite in self.obstacles:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0: self.hitbox.bottom = sprite.rect.top  # moving down
                    if self.direction.y < 0: self.hitbox.top = sprite.rect.bottom  # moving up

    def move(self, speed: int):
        if self.direction.magnitude(): self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision(HORIZONTAL)

        self.hitbox.y += self.direction.y * speed
        self.collision(VERTICAL)

        self.rect.center = self.hitbox.center

    @staticmethod
    def getFlickerValue(): return 255 if sin(pg.time.get_ticks()) >= 0 else 0
