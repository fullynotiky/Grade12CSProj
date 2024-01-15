import pygame as pg

from random import choice, randint
from camera import CameraGroup
from enemy import Enemy
from spells import SpellPlayer
from particleEffect import AnimationPlayer
from player import Player
from tile import Tile
from ui import UI
from upgrade import Upgrade
from weapon import Weapon
from leavesOverlay import Leaves
from startMenu import StartMenu
from gameData import GameData
from globals import *
from utils import *


class Level:
    def __init__(self, game):

        self.gameHighscore = 0
        self.gameData = None
        self.game = game
        self.dayNum = 0
        self.alpha = 0
        self.enemies = []
        self.inGameStart = False
        self.inStartMenu = False
        self.inSettingsMenu = False
        self.gamePaused = False
        self.inGame = False
        self.gameWon = False
        self.loggedIn = False
        self.dataWritten = False
        self.username = self.game.username
        self.playerHighscore = 0
        self.display = pg.display.get_surface()
        self.dayNightSurf = pg.Surface((WIDTH, HEIGHT))
        self.dayNightSurf.fill('black')
        self.dayNightSurf.set_alpha(self.alpha)

        self.controls = ({'Space': 'Upgrade',
                          'A': 'Navigate Left',
                          'D': 'Navigate Right'},
                         {'Q': 'Change weapon',
                          'Space': 'Attack',
                          'E': 'Change Spell',
                          'C': 'Upgrade Menu',
                          'Esc': 'Exit',
                          'R Control': 'Use Spell'})

        self.visibleSprites = CameraGroup()
        self.obstacleSprites = pg.sprite.Group()
        self.attackSprites = pg.sprite.Group()
        self.attackableSprites = pg.sprite.Group()

        self.player = Player((2000, 1430),
                             self.visibleSprites,
                             self.obstacleSprites,
                             self.createWeapon,
                             self.destroyWeapon,
                             self.createMagic,
                             self)

        self.leavesOverlay = Leaves(self.visibleSprites)

        self.currentWeapon = None
        self.drawMap()

        self.startMenu = StartMenu(self)
        self.ui = UI(self.player, self.startMenu)
        self.upgrade = Upgrade(self.player)
        self.font = pg.font.Font(FONT_PATH, FONT_SIZE)

        self.x, self.y = self.visibleSprites.getOffset(self.player)

        self.animationPlayer = AnimationPlayer()
        self.magicPlayer = SpellPlayer(self.animationPlayer, self.player)

        self.deadPlayerSurf = pg.image.load('graphics\\ui\\dead.png').convert_alpha()
        self.deadPlayerSurf = pg.transform.scale(self.deadPlayerSurf, (350, 360))
        self.deadPlayerRect = self.deadPlayerSurf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        self.gameOverSurf = self.startMenu.largeFont.render('GAME OVER', True, 'blue')
        self.gameOverRect = self.gameOverSurf.get_rect(center=(WIDTH // 2, 100))

        self.youDiedSurf = self.startMenu.mediumSmallFont.render('You Died!', True, 'blue')
        self.youDiedRect = self.youDiedSurf.get_rect(center=(WIDTH // 2, 200))

        self.youWonSurf = self.startMenu.mediumFont.render('YOU WON!', True, 'white')
        self.youWonRect = self.youWonSurf.get_rect(center=(WIDTH // 2, 250))

        self.wonSpriteSurf = pg.transform.scale(self.player.image, (300, 300))
        self.wonSpriteRect = self.wonSpriteSurf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    def drawMap(self):
        layouts = {
            'boundary': getLayout('map\\map_FloorBlocks.csv'),
            'grass': getLayout('map\\map_Grass.csv'),
            'object': getLayout('map\\map_Objects.csv'),
            'entities': getLayout('map\\map_Entities.csv')
        }

        graphics = {'grass': getFolder('graphics\\grass'), 'object': getFolder('graphics\\objects')}

        for type, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, element in enumerate(row):
                    if element != '-1':
                        x, y = j * TILESIZE, i * TILESIZE

                        if type == 'boundary': Tile((x, y),
                                                    (self.obstacleSprites,),
                                                    'invisible')

                        if type == 'grass': Tile((x, y),
                                                 (self.visibleSprites, self.obstacleSprites, self.attackableSprites),
                                                 'grass',
                                                 choice(graphics['grass']))

                        if type == 'object': Tile((x, y),
                                                  (self.visibleSprites, self.obstacleSprites),
                                                  'object',
                                                  graphics['object'][int(element)])

                        if type == 'entities':
                            match element:
                                case '390':
                                    monsterType = 'bamboo'
                                case '392':
                                    monsterType = 'raccoon'
                                case TypeError:
                                    monsterType = 'squid'

                            self.enemies.append(Enemy((self.visibleSprites, self.attackableSprites),
                                                      monsterType,
                                                      (x, y),
                                                      self.obstacleSprites,
                                                      self.player,
                                                      self.damageToPlayer,
                                                      self.deathParticles,
                                                      self.updatePlayerEXP))

    def createWeapon(self):
        self.currentWeapon = Weapon((self.visibleSprites, self.attackSprites), self.player)

    def toggleUpgradeMenu(self): self.gamePaused = not self.gamePaused

    def createMagic(self, style: str, strength: int, cost: int):
        if style == 'heal': self.magicPlayer.heal(strength, cost, (self.visibleSprites,))
        if style == 'flame': self.magicPlayer.flame(cost, (self.visibleSprites, self.attackSprites))

    def destroyWeapon(self):
        if self.currentWeapon: self.currentWeapon.kill()
        self.currentWeapon = None

    def playerAttack(self):
        if self.attackSprites:
            for sprite in self.attackSprites:
                collidingSprites = pg.sprite.spritecollide(sprite, self.attackableSprites, False)

                if collidingSprites:
                    for target in collidingSprites:
                        if target.spriteType == 'grass':
                            for _ in range(randint(3, 6)):
                                self.animationPlayer.grassParticles(target.rect.center - pg.Vector2(0, 50),
                                                                    (self.visibleSprites,))
                            target.kill()
                        else:
                            target.getDamage(self.player, sprite.spriteType)

    def damageToPlayer(self, amount, attackType):
        if self.player.isVulnerable:
            self.player.health -= amount
            self.player.isVulnerable = False
            self.player.damageTime = pg.time.get_ticks()

            self.animationPlayer.createParticles(attackType,
                                                 self.player.rect.center,
                                                 (self.visibleSprites,))

    def deathParticles(self, pos, particleType):
        self.animationPlayer.createParticles(particleType, pos, (self.visibleSprites,))

    def updatePlayerEXP(self, amount: int):
        self.player.exp += amount

    def displayScore(self):
        scoreSurf = self.font.render(f'SCORE: {abs(int(self.player.score))}', True, 'white')
        pg.draw.rect(self.display, 'black', (1125, 15, 150, 23))
        self.display.blit(scoreSurf, (1130, 14))

    def dayNightFunc(self):
        time = pg.time.get_ticks()
        self.dayNum = time // 30000  # every 30sec

        self.alpha += 0.37
        if self.alpha >= 180: self.alpha = -180

        self.dayNightSurf.set_alpha(abs(self.alpha))
        self.display.blit(self.dayNightSurf, (0, 0))

    def gameEndOverlay(self):
        self.startMenu.transparentOverlay.set_alpha(200)
        self.display.blit(self.startMenu.transparentOverlay, (0, 0))
        self.display.blit(self.startMenu.exitButtonSurf, self.startMenu.exitButtonRect)
        self.display.blit(self.startMenu.muteButtonSurf, self.startMenu.muteButtonRect)
        self.display.blit(self.startMenu.muteButtonIconSurf, self.startMenu.muteButtonIconRect)

        self.display.blit(self.player.finalScoreTextSurf, self.player.finalScoreTextRect)

        finalScoreSurf = self.player.font.render(str(int(abs(self.player.score))), True, 'white')
        finalScoreRect = finalScoreSurf.get_rect(center=(180, 430))

        self.display.blit(finalScoreSurf, finalScoreRect)

        self.display.blit(self.startMenu.userNameSurf, self.startMenu.userNameRect.move(0, 100))
        self.display.blit(self.startMenu.highScoreSurf, self.startMenu.highScoreRect.move(0, 100))

    def endGameFunc(self):
        if self.player.score > self.playerHighscore: self.playerHighscore = self.player.score
        self.gameWon = True
        self.startMenu.highScoreSurf = self.startMenu.smallFont.render(f'HIGHSCORE: {self.playerHighscore}', True, 'white')
        self.gameEndOverlay()
        self.inGame = self.inStartMenu = self.inGameStart = self.gamePaused = False
        self.display.blit(self.startMenu.gameNameSurf, self.startMenu.gameNameRect)
        self.display.blit(self.youWonSurf, self.youWonRect)
        self.display.blit(self.wonSpriteSurf, self.wonSpriteRect)

    def playerDeath(self):
        self.gameEndOverlay()
        self.display.blit(self.deadPlayerSurf, self.deadPlayerRect)
        self.display.blit(self.gameOverSurf, self.gameOverRect)
        self.display.blit(self.youDiedSurf, self.youDiedRect)

    def loginFunc(self, username: str):
        self.loggedIn = self.inStartMenu = self.inGameStart = True
        self.startMenu.setUser(username)
        self.gameData = GameData(username)
        self.playerHighscore = self.gameData.playerHighscore
        self.gameHighscore = self.gameData.gameHighscore
        self.startMenu.highScoreSurf = self.startMenu.smallFont.render(f'HIGHSCORE: {self.playerHighscore}', True, 'white')

    def exitFunc(self):
        if (not self.dataWritten) and (self.gameWon or self.player.died or self.inGame): self.gameData.end(self.player)
        pg.quit()
        exit()

    def run(self):
        currVolume = self.startMenu.volume / 100

        self.player.weaponAttackSound.set_volume(currVolume)
        self.game.mainSound.set_volume(currVolume)

        for enemy in self.enemies:
            enemy.hitSound.set_volume(currVolume)
            enemy.deathSound.set_volume(currVolume)
            enemy.attackSound.set_volume(currVolume)

        if self.loggedIn:
            self.visibleSprites.draw(self.player)
            self.ui.display()

            if self.dayNum >= 4:
                self.endGameFunc()  # 4days to win

            if self.inGameStart or self.inSettingsMenu: self.startMenu.run()

            elif self.gamePaused:
                pos1 = 450
                for k, c in self.controls[0].items():
                    f = font.render(str(k + ' : ' + c), True, 'White')
                    width, height = f.get_rect().size

                    s = pg.Surface(size=(width + 2 * padX, height + 2 * padY))
                    s.blit(f, (padX, padX))

                    display.get_surface().blit(s, (pos1, 9))

                    pos1 = pos1 + width + 2 * padX + 10

                self.upgrade.display()

            elif self.inGame and self.inSettingsMenu:
                self.inStartMenu = False
                self.ui.displaySettingsButton()
                self.displayScore()

            elif self.player.died:
                self.playerDeath()
                self.displayScore()

            else:
                self.displayScore()
                self.visibleSprites.update()
                self.visibleSprites.updateEnemy(self.player)
                self.playerAttack()
                self.leavesOverlay.run()

                if self.loggedIn and self.inGame: self.dayNightFunc()

                pos2 = 225
                for k, c in self.controls[1].items():
                    f = font.render(str(k + ' : ' + c), True, 'White')
                    width, height = f.get_rect().size

                    s = pg.Surface(size=(width + 2 * padX, height + 2 * padY))
                    s.blit(f, (padX, padX))
                    display.get_surface().blit(s, (pos2, 9))

                    pos2 = pos2 + width + 2 * padX + 10

        else: self.startMenu.displayLoginPage(self.game.username)
