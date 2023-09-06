from os import chdir
from random import randint

import pygame as pg

from particleEffect import AnimationPlayer
from player import Player
from settings import *

chdir('E:\\Harshith\\Python Programming\\School Stuff\\Grade12CSProj')


class MagicPlayer:
    def __init__(self, animationPlayer: AnimationPlayer, player: Player):
        self.animationPlayer = animationPlayer
        self.player = player

        self.sounds = {
            HEAL: pg.mixer.Sound('audio\\heal.wav'),
            FLAME: pg.mixer.Sound('audio\\Fire.wav')
        }

    def heal(self, strength: int, cost: int, groups):
        if self.player.energy >= cost:
            self.player.health += strength
            self.player.energy -= cost

            if self.player.health >= self.player.stats['health']:
                self.player.health = self.player.stats['health']

            self.sounds[HEAL].play()
            self.animationPlayer.createParticles('aura',
                                                 self.player.rect.center,
                                                 groups)
            self.animationPlayer.createParticles('heal',
                                                 self.player.rect.center + pg.Vector2(0, -50),
                                                 groups)

    def flame(self, cost: int, groups):
        if self.player.energy >= cost:
            self.player.energy -= cost

            if self.player.state.split('_')[0] == UP:
                direc = pg.Vector2(0, -1)
            elif self.player.state.split('_')[0] == DOWN:
                direc = pg.Vector2(0, 1)
            elif self.player.state.split('_')[0] == RIGHT:
                direc = pg.Vector2(1, 0)
            else:
                direc = pg.Vector2(-1, 0)

            self.sounds[FLAME].play()

            for i in range(1, 5):
                if direc.x:
                    xOffset = direc.x * i * TILESIZE
                    x = self.player.rect.centerx + xOffset + randint(-TILESIZE // 5, TILESIZE // 5)
                    y = self.player.rect.centery + randint(-TILESIZE // 5, TILESIZE // 5)
                    self.animationPlayer.createParticles(FLAME, (x, y), groups)

                else:
                    yOffset = direc.y * i * TILESIZE
                    x = self.player.rect.centerx + randint(-TILESIZE // 5, TILESIZE // 5)
                    y = self.player.rect.centery + yOffset + randint(-TILESIZE // 5, TILESIZE // 5)
                    self.animationPlayer.createParticles(FLAME, (x, y), groups)
