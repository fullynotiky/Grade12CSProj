import pygame as pg

from os import chdir
from level import Level
from globals import *


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Grade12 CS Proj")

        self.username = ''
        self.clickCooldown = 300

        self.clock = pg.time.Clock()
        self.level = Level(self)
        self.startMenu = self.level.startMenu

        self.mainSound = pg.mixer.Sound('audio\\main.ogg')
        self.mainSound.set_volume(self.startMenu.volume/100)
        self.mainSound.play(-1)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.level.exitFunc()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_c and (self.level.player.died or self.level.gameWon or self.level.loggedIn):
                        self.level.toggleUpgradeMenu()

                    if not self.level.loggedIn:
                        key = event.unicode
                        if key.isalnum() and ord(key) != 13 and len(self.username) <= 15: self.username += key

                        if event.key == pg.K_RETURN and len(self.username) < 15: self.level.loginFunc(self.username)

                        if event.key == pg.K_BACKSPACE: self.username = self.username[:-2]

                if event.type == pg.MOUSEBUTTONDOWN:
                    currTime = pg.time.get_ticks()
                    pos = pg.mouse.get_pos()

                    if self.level.inStartMenu:
                        for index, rect in enumerate(self.startMenu.startMenuRects):
                            if rect.collidepoint(pos) and currTime - self.startMenu.clickTime > self.clickCooldown:
                                self.startMenu.startMenuCommands[index]()

                    if self.level.inSettingsMenu or self.level.player.died or self.level.gameWon:
                        for index, rect in enumerate(self.startMenu.settingsMenuRects):
                            if rect.collidepoint(pos) and currTime - self.startMenu.clickTime > self.clickCooldown:
                                self.startMenu.settingsMenuCommands[index]()

                    if self.level.inGame and self.level.ui.settingsRect.collidepoint(pos): self.level.startMenu.settingsFunc()
            self.level.run()
            pg.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
