from random import choice

import pygame as pg

from globals import *
from utils import *


def reflectImages(frames): return [pg.transform.flip(frame, True, False) for frame in frames]


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'flame': getFolder('graphics/particles/flame/frames'),
            'aura': getFolder('graphics/particles/aura'),
            'heal': getFolder('graphics/particles/heal/frames'),

            'claw': getFolder('graphics/particles/claw'),
            'slash': getFolder('graphics/particles/slash'),
            'sparkle': getFolder('graphics/particles/sparkle'),
            'leaf_attack': getFolder('graphics/particles/leaf_attack'),
            'thunder': getFolder('graphics/particles/thunder'),

            'squid': getFolder('graphics/particles/smoke_orange'),
            'raccoon': getFolder('graphics/particles/raccoon'),
            'spirit': getFolder('graphics/particles/nova'),
            'bamboo': getFolder('graphics/particles/bamboo'),

            'leaf': (
                getFolder('graphics/particles/leaf1'),
                getFolder('graphics/particles/leaf2'),
                getFolder('graphics/particles/leaf3'),
                getFolder('graphics/particles/leaf4'),
                getFolder('graphics/particles/leaf5'),
                getFolder('graphics/particles/leaf6'),
                reflectImages(getFolder('graphics/particles/leaf1')),
                reflectImages(getFolder('graphics/particles/leaf2')),
                reflectImages(getFolder('graphics/particles/leaf3')),
                reflectImages(getFolder('graphics/particles/leaf4')),
                reflectImages(getFolder('graphics/particles/leaf5')),
                reflectImages(getFolder('graphics/particles/leaf6'))
            )
        }

    def grassParticles(self, pos, groups): ParticleEffect(pos, choice(self.frames['leaf']), groups)

    def createParticles(self, animationType, pos, groups): ParticleEffect(pos, (self.frames[animationType]), groups)


class ParticleEffect(pg.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)

        self.spriteType = 'spell'
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.frames = frames
        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frameIndex)]

    def update(self):
        self.animate()
