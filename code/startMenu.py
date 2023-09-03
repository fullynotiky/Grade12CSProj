import pygame as pg
from upgrade import Item
from settings import *
from os import chdir

chdir('E:\\Harshith\\Python Programming\\School Stuff\\School Project\\graphics')


def exitGame():
    pg.quit()
    exit()


class StartMenu:
    def __init__(self, level):
        self.displaySurf = pg.display.get_surface()
        self.largeFont = pg.font.Font(FONT, FONT_SIZE + 125)
        self.mediumFont = pg.font.Font(FONT, FONT_SIZE + 45)
        self.mediumSmallFont = pg.font.Font(FONT, FONT_SIZE + 25)
        self.smallFont = pg.font.Font(FONT, FONT_SIZE + 5)

        self.level = level

        self.frameIndex = 0
        self.animationSpeed = 0.15

        self.gameNameSurf = self.largeFont.render('ZELDA', True, 'blue')
        self.gameNameSurf = pg.transform.scale(self.gameNameSurf, (420, 150))
        self.gameNameRect = self.gameNameSurf.get_rect(center=(650, 150))

        self.playButtonSurf = pg.image.load('graphics\\startmenu\\3.png').convert_alpha()
        self.playButtonSurf = pg.transform.scale(self.playButtonSurf, (400, 120))
        self.playButtonRect = self.playButtonSurf.get_rect(center=(WIDTH//2, 500))

        self.settingsSurf = self.mediumFont.render('SETTINGS', True, 'white')
        self.settingsSurf = pg.transform.scale(self.settingsSurf, (220, 55))
        self.settingsRect = self.settingsSurf.get_rect(center=(120, 500))

        self.settingsSelectedSurf = pg.transform.scale(pg.image.load('graphics\\ui\\selected.png').convert_alpha(),
                                                       (305, 12))
        self.settingsSelectedRect = self.settingsRect.move((-45, 50))

        self.userNameSurf = self.smallFont.render('USER: ', True, 'green')
        self.userNameRect = self.userNameSurf.get_rect(topleft=(10, 70))
        self.highScoreSurf = self.smallFont.render(f'HIGHSCORE: {10}', True, 'white')
        self.highScoreRect = self.highScoreSurf.get_rect(topleft=(10, 100))

        self.spriteSurf = pg.transform.scale(pg.image.load('graphics\\startmenu\\1.png').convert_alpha(), (300, 320))
        self.spriteRect = self.spriteSurf.get_rect(center=(1100, 320))

        self.volumeTextSurf = self.mediumSmallFont.render('VOLUME', True, 'black')

        self.volumeFrameSurf = self.muteButtonSurf = pg.image.load('graphics\\ui\\volume_frame.png').convert_alpha()
        self.volumeFrameSurf = pg.transform.scale(self.volumeFrameSurf, (400, 700))
        self.volumeFrameSurf.blit(self.volumeTextSurf, (110, 580))
        self.volumeFrameRect = self.volumeFrameSurf.get_rect(center=(WIDTH//2-20, HEIGHT//2))

        self.muteButtonIconSurf = pg.transform.scale(pg.image.load('graphics\\startmenu\\mute.png').convert_alpha(), (60, 60))
        self.muteButtonIconRect = self.muteButtonIconSurf.get_rect(center=(1000, 295))
        self.muteButtonSurf = pg.transform.scale(pg.image.load('graphics\\startmenu\\button.png').convert_alpha(), (100, 100))
        self.muteButtonRect = self.muteButtonSurf.get_rect(center=(1000, 300))

        self.exitTextSurf = self.mediumFont.render('EXIT', True, 'black')
        self.exitButtonSurf = pg.image.load('graphics\\startmenu\\button.png').convert_alpha()
        self.exitButtonSurf.blit(self.exitTextSurf, (42, 0))
        self.exitButtonRect = self.exitButtonSurf.get_rect(center=(1000, 500))

        self.startMenuRects = (self.settingsRect, self.playButtonRect)
        self.startMenuCommands = (self.settingsFunc, self.playFunc)

        self.settingsMenuRects = (self.settingsRect, self.muteButtonRect, self.exitButtonRect)
        self.settingsMenuCommands = (self.settingsFunc, self.muteFunc, exitGame)

        self.transparentOverlay = pg.Surface((WIDTH, HEIGHT))
        self.transparentOverlay.fill('black')
        self.transparentOverlay.set_alpha(180)

        self.canClick = True
        self.clickCooldown = 300
        self.clickTime = 0

        self.volume = 10
        self.volume2 = self.volume
        self.maxVolume = 100
        self.volumeCoolDown = 100

        self.level.inGame = False

    def playFunc(self):
        self.level.inGameStart = False
        self.level.inGame = True

    def muteFunc(self):
        if self.volume:
            self.volume2 = self.volume
            self.volume = 0
        else: self.volume = self.volume2

    def input(self):
        keys = pg.key.get_pressed()
        currTime = pg.time.get_ticks()

        if currTime - self.clickTime >= self.volumeCoolDown:
            if keys[pg.K_UP]:
                self.volume += 5
                self.clickTime = pg.time.get_ticks()
                if self.volume >= 100:
                    self.volume = 100

            if keys[pg.K_DOWN]:
                self.volume -= 5
                self.clickTime = pg.time.get_ticks()
                if self.volume <= 0:
                    self.volume = 0

    def settingsFunc(self):
        self.clickTime = pg.time.get_ticks()
        self.level.inStartMenu = not self.level.inStartMenu
        self.level.inSettingsMenu = not self.level.inSettingsMenu

    def updateVolume(self, value: int):
        barLen = self.volumeFrameRect.bottom - self.volumeFrameRect.top - 200
        relValue = (value/self.maxVolume) * barLen
        maxValue = 420

        if relValue >= maxValue: relValue = maxValue

        pg.draw.rect(self.displaySurf, 'black', (601, 500-relValue, 40, 15))
        pg.draw.line(self.volumeFrameSurf, 'black', (200, 100), (200, 560), 6)

    def displayStartMenu(self):
        self.displaySurf.blit(self.gameNameSurf, self.gameNameRect)
        self.displaySurf.blit(self.playButtonSurf, self.playButtonRect)
        self.displaySurf.blit(self.spriteSurf, self.spriteRect)

    def displaySettingsMenu(self):
        self.displaySurf.blit(self.volumeFrameSurf, self.volumeFrameRect)
        self.displaySurf.blit(self.exitButtonSurf, self.exitButtonRect)
        self.displaySurf.blit(self.muteButtonSurf, self.muteButtonRect)
        self.displaySurf.blit(self.muteButtonIconSurf, self.muteButtonIconRect)
        self.updateVolume(self.volume)

    def displayMainOverlay(self, settingsSelected: bool):
        self.displaySurf.blit(self.transparentOverlay, (0, 0))
        self.displaySurf.blit(self.userNameSurf, self.userNameRect)
        self.displaySurf.blit(self.highScoreSurf, self.highScoreRect)
        self.displaySurf.blit(self.settingsSurf, self.settingsRect)

        if settingsSelected: self.displaySurf.blit(self.settingsSelectedSurf, self.settingsSelectedRect)

    def run(self):
        if self.level.inGameStart:
            self.displayMainOverlay(self.level.inSettingsMenu)

            if self.level.inStartMenu:
                self.displayStartMenu()

        if self.level.inSettingsMenu:
            self.displaySettingsMenu()
        self.input()
