import pygame as pg

from player import Player
from startMenu import StartMenu
from globals import *


class UI:
    def __init__(self, player: Player, startMenu: StartMenu):
        self.startMenu = startMenu

        self.displaySurf = pg.display.get_surface()
        self.font = pg.font.Font(FONT_PATH, FONT_SIZE)

        self.player = player

        self.healthBarRect = pg.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energyBarRect = pg.Rect(10, 35, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.weaponGraphics = [pg.image.load(weapon['graphic']).convert_alpha() for weapon in WEAPONS.values()]
        self.magicGraphics = [pg.image.load(magic['graphic']).convert_alpha() for magic in SPELLS.values()]

        self.settingsSurf = pg.transform.scale(self.startMenu.settingsSurf, (100, 30))
        self.settingsRect = self.settingsSurf.get_rect(center=(1200, 55))

    def displayBar(self, value: int, maxValue, rect: pg.Rect, color):
        pg.draw.rect(self.displaySurf, UI_BG_COLOR, rect)

        ratio = value / maxValue
        width = rect.width * ratio
        newRect = rect.copy()
        newRect.width = width

        pg.draw.rect(self.displaySurf, color, newRect)  # filling

        pg.draw.rect(self.displaySurf, UI_BORDER_COLOR, newRect, 3)  # border

    def displaySettingsButton(self):
        pg.draw.rect(self.displaySurf, 'black', (1145, 45, 110, 25))
        self.displaySurf.blit(self.settingsSurf, self.settingsRect)

    def displayExp(self):
        textSurf = self.font.render(str(int(self.player.exp)), True, TEXT_COLOR)
        textRect = textSurf.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))

        newRect = textRect.inflate(10, 10)
        pg.draw.rect(self.displaySurf, UI_BG_COLOR, newRect)  # background
        self.displaySurf.blit(textSurf, textRect)
        pg.draw.rect(self.displaySurf, UI_BORDER_COLOR, newRect, 5)  # border

    def selectedBox(self, left: int, top: int) -> pg.Rect:
        rect = pg.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pg.draw.rect(self.displaySurf, UI_BG_COLOR, rect)

        if not (self.player.canChangeWeapon and self.player.canChangeMagic):
            pg.draw.rect(self.displaySurf, UI_BORDER_COLOR_ACTIVE, rect, 5)

        else:
            pg.draw.rect(self.displaySurf, UI_BORDER_COLOR, rect, 5)
        return rect

    def weaponOverlay(self):
        rect = self.selectedBox(10, 570)
        weaponSurf = self.weaponGraphics[self.player.weaponIndex]
        weaponRect = weaponSurf.get_rect(center=rect.center)

        self.displaySurf.blit(weaponSurf, weaponRect)

    def magicOverlay(self):
        rect = self.selectedBox(15 + ITEM_BOX_SIZE, 570)
        magicSurf = self.magicGraphics[self.player.magicIndex]
        magicRect = magicSurf.get_rect(center=rect.center)

        self.displaySurf.blit(magicSurf, magicRect)

    def display(self):
        self.displayBar(self.player.health, self.player.stats['health'], self.healthBarRect, HEALTH_COLOR)
        self.displayBar(self.player.energy, self.player.stats['energy'], self.energyBarRect, ENERGY_COLOR)

        self.displaySettingsButton()
        self.displayExp()
        self.weaponOverlay()
        self.magicOverlay()
        self.startMenu.level.displayScore()
