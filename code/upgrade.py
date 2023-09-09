import pygame as pg

from player import Player
from globals import *


class Upgrade:
    def __init__(self, player: Player):
        self.items = None

        self.displaySurf = pg.display.get_surface()
        self.player = player

        self.nAttributes = len(self.player.stats)
        self.attributeNames = tuple(self.player.stats)
        self.maxValues = tuple(self.player.maxStats.values())
        self.font = pg.font.Font(FONT_PATH, FONT_SIZE)

        self.selectedIndex = 0
        self.selectionTime = 0
        self.selectionCooldown = 200
        self.canMove = True

        self.gameHeight = HEIGHT
        self.gameWidth = WIDTH
        self.height = self.gameHeight * 0.8
        self.width = self.gameWidth // (self.nAttributes + 1)

        self.createItem()

    def input(self):
        keys = pg.key.get_pressed()

        if self.canMove:
            if keys[pg.K_d] and self.selectedIndex < self.nAttributes - 1:
                self.selectedIndex += 1
                self.selectionTime = pg.time.get_ticks()
                self.canMove = False
            elif keys[pg.K_a] and self.selectedIndex >= 1:
                self.selectedIndex -= 1
                self.selectionTime = pg.time.get_ticks()
                self.canMove = False

            if keys[pg.K_SPACE]:
                self.selectionTime = pg.time.get_ticks()
                self.canMove = False
                self.items[self.selectedIndex].updateBars(self.player)

    def cooldown(self):
        if not self.canMove:
            currTime = pg.time.get_ticks()
            if currTime - self.selectionTime >= self.selectionCooldown: self.canMove = True

    def createItem(self):
        self.items = []

        for item in range(self.nAttributes):
            padding = self.gameWidth // self.nAttributes
            left = (item * padding) + (padding - self.gameWidth) // 2 + 535

            top = self.gameHeight * 0.1

            item = Item(left, top, self.width, self.height, item, self.font)
            self.items.append(item)

    def display(self):
        self.input()
        self.cooldown()

        for index, item in enumerate(self.items):
            name = self.attributeNames[index]
            value = tuple(self.player.stats.values())[index]
            maxValue = self.maxValues[index]
            cost = tuple(self.player.upgradeCosts.values())[index]

            item.display(self.selectedIndex, name, value, maxValue, cost)


class Item:
    def __init__(self, len: int, top: int, width: int, height: int, index: int, font: pg.font.Font):
        self.displaySurf = pg.display.get_surface()
        self.rect = pg.Rect(len, top, width, height)
        self.index = index
        self.font = font

    def displayNames(self, name: str, cost: int, selected: bool):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        titleSurf = self.font.render(str(name), False, color)
        titleRect = titleSurf.get_rect(midtop=self.rect.midtop + pg.Vector2(0, 20))

        costSurf = self.font.render(str(int(cost)), False, color)
        costRect = costSurf.get_rect(midbottom=self.rect.midbottom + pg.Vector2(0, -20))

        self.displaySurf.blit(titleSurf, titleRect)
        self.displaySurf.blit(costSurf, costRect)

    def displayBar(self, value: int, maxValue: int, selected: bool):
        top = self.rect.midtop + pg.Vector2(0, 60)
        bottom = self.rect.midbottom + pg.Vector2(0, -60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        barLen = bottom.y - top.y
        relValue = (value / maxValue) * barLen
        pointerRect = pg.Rect(top.x - 15, bottom.y - relValue, 30, 10)

        pg.draw.line(self.displaySurf, color, top, bottom, 6)
        pg.draw.rect(self.displaySurf, color, pointerRect)

    def updateBars(self, player: Player):
        upgradeAttr = tuple(player.stats)[self.index]

        cost = player.upgradeCosts[upgradeAttr]
        maxUpgrade = player.maxStats[upgradeAttr]
        if player.exp >= cost and player.stats[upgradeAttr] < maxUpgrade:
            player.exp -= cost
            player.inExp -= cost
            player.stats[upgradeAttr] *= 1.2
            player.upgradeCosts[upgradeAttr] *= 1.2

        if player.stats[upgradeAttr] > maxUpgrade: player.stats[upgradeAttr] = maxUpgrade

    def display(self, selectedNum: int, name: str, value: int, maxValue: int, cost: int):
        selected = self.index == selectedNum

        if selected:
            pg.draw.rect(self.displaySurf, UI_BORDER_COLOR_ACTIVE, self.rect)
            pg.draw.rect(self.displaySurf, UI_BG_COLOR, self.rect, 5)

        else:
            pg.draw.rect(self.displaySurf, UI_BG_COLOR, self.rect)
            pg.draw.rect(self.displaySurf, UI_BORDER_COLOR, self.rect, 5)

        self.displayNames(name, cost, selected)
        self.displayBar(value, maxValue, selected)
