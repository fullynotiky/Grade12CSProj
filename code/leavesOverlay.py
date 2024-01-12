import pygame as pg

from utils import *
from globals import *


class Leaves(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.rect = pg.Rect(0, 0, WIDTH, HEIGHT)
        self.leavesFrames = getFolder('graphics\\leaves')
        self.frameIndex = 0
        self.image = self.leavesFrames[self.frameIndex]
        self.displaySurf = pg.display.get_surface()
        self.animationSpeed = 0.1

    def leavesOverlay(self):
        frame = self.leavesFrames[int(self.frameIndex)]
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.leavesFrames): self.frameIndex = 0

        self.image = self.leavesFrames[int(self.frameIndex)]
        self.image.set_alpha(200)
        self.image = pg.transform.scale(self.image, (WIDTH-10, HEIGHT-10))
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.displaySurf.blit(self.image, self.rect)

    def run(self): self.leavesOverlay()
