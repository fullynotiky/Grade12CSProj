import pygame as pg

from random import randint
from particleEffect import AnimationPlayer
from player import Player
from globals import *


class SpellPlayer:
    def __init__(self, animationPlayer: AnimationPlayer, player: Player):
        self.animationPlayer = animationPlayer
        self.player = player

        self.sounds = {
            'heal': pg.mixer.Sound('audio\\heal.wav'),
            'flame': pg.mixer.Sound('audio\\Fire.wav')
        }

    def heal(self, strength: int, cost: int, groups):
        if self.player.energy >= cost:
            self.player.health += strength
            self.player.energy -= cost

            if self.player.health >= self.player.stats['health']: self.player.health = self.player.stats['health']

            self.sounds['heal'].play()
            self.animationPlayer.createParticles('aura',
                                                 self.player.rect.center,
                                                 groups)
            self.animationPlayer.createParticles('heal',
                                                 self.player.rect.center + pg.Vector2(0, -50),
                                                 groups)

    def flame(self, cost: int, groups):
        if self.player.energy >= cost:
            self.player.energy -= cost

            if self.player.state.split('_')[0] == 'up': direc = pg.Vector2(0, -1)
            elif self.player.state.split('_')[0] == 'down': direc = pg.Vector2(0, 1)
            elif self.player.state.split('_')[0] == 'right': direc = pg.Vector2(1, 0)
            else: direc = pg.Vector2(-1, 0)

            self.sounds['flame'].play()

            for i in range(1, 5):
                if direc.x:
                    xOffset = direc.x * i * TILESIZE
                    x = self.player.rect.centerx + xOffset + randint(-TILESIZE // 5, TILESIZE // 5)
                    y = self.player.rect.centery + randint(-TILESIZE // 5, TILESIZE // 5)
                    self.animationPlayer.createParticles('flame', (x, y), groups)

                else:
                    yOffset = direc.y * i * TILESIZE
                    x = self.player.rect.centerx + randint(-TILESIZE // 5, TILESIZE // 5)
                    y = self.player.rect.centery + yOffset + randint(-TILESIZE // 5, TILESIZE // 5)
                    self.animationPlayer.createParticles('flame', (x, y), groups)
