from os import chdir

import pygame as pg

from level import Level
from startMenu import StartMenu
from settings import *

chdir('E:\\Harshith\\Python Programming\\School Stuff\\School Project')


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Zelda')

        self.clock = pg.time.Clock()
        self.level = Level()
        self.startMenu = StartMenu(self.level)

        self.mainSound = pg.mixer.Sound('audio\\main.ogg')
        self.mainSound.set_volume(self.startMenu.volume/100)
        self.mainSound.play(-1)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_c and not self.level.player.died:
                        self.level.inGame = not self.level.inGame
                        self.level.toggleUpgradeMenu()

                    if event.key == pg.K_p:
                        pg.quit()
                        exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    currTime = pg.time.get_ticks()
                    pos = pg.mouse.get_pos()

                    if self.level.inStartMenu:
                        for index, rect in enumerate(self.startMenu.startMenuRects):
                            if rect.collidepoint(pos) and currTime - self.startMenu.clickTime > self.startMenu.clickCooldown:
                                self.startMenu.startMenuCommands[index]()

                    if self.level.inSettingsMenu or self.level.player.died:
                        for index, rect in enumerate(self.startMenu.settingsMenuRects):
                            if rect.collidepoint(pos) and currTime - self.startMenu.clickTime > self.startMenu.clickCooldown:
                                self.startMenu.settingsMenuCommands[index]()

                    if self.level.inGame:
                        if self.level.ui.settingsRect.collidepoint(pos):
                            self.level.startMenu.settingsFunc()

            self.level.run()

            currVolume = self.startMenu.volume / 100

            self.mainSound.set_volume(currVolume)
            self.level.player.weaponAttackSound.set_volume(currVolume)

            for enemy in self.level.enemies:
                enemy.hitSound.set_volume(currVolume)
                enemy.deathSound.set_volume(currVolume)
                enemy.attackSound.set_volume(currVolume)

            if self.level.inGameStart or self.level.inSettingsMenu: self.startMenu.run()

            pg.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
