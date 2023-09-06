from os import chdir
from random import choice, randint

import pygame as pg

from camera import CameraGroup
from enemy import Enemy
from magic import MagicPlayer
from particleEffect import AnimationPlayer
from player import Player
from settings import *
from tile import Tile
from ui import UI
from upgrade import Upgrade
from utils import *
from debug import debug
from weapon import Weapon
from leavesOverlay import Leaves
from startMenu import StartMenu

chdir('E:\\Harshith\\Python Programming\\School Stuff\\Grade12CSProj')


class Level:
    def __init__(self, game) -> None:

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
        self.username = self.game.username
        self.highscore = 0
        self.display = pg.display.get_surface()
        self.dayNightSurf = pg.Surface((WIDTH, HEIGHT))
        self.dayNightSurf.fill('black')
        self.dayNightSurf.set_alpha(self.alpha)

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
        self.font = pg.font.Font(FONT, FONT_SIZE)

        self.x, self.y = self.visibleSprites.getOffset(self.player)

        self.animationPlayer = AnimationPlayer()
        self.magicPlayer = MagicPlayer(self.animationPlayer, self.player)

        self.deadPlayerSurf = pg.image.load('graphics\\ui\\dead.png').convert_alpha()
        self.deadPlayerSurf = pg.transform.scale(self.deadPlayerSurf, (350, 360))
        self.deadPlayerRect = self.deadPlayerSurf.get_rect(center=(WIDTH//2, HEIGHT//2+50))

        self.gameOverSurf = self.startMenu.largeFont.render('GAME OVER', True, 'blue')
        self.gameOverRect = self.gameOverSurf.get_rect(center=(WIDTH//2, 100))

        self.youDiedSurf = self.startMenu.mediumSmallFont.render('You Died!', True, 'blue')
        self.youDiedRect = self.youDiedSurf.get_rect(center=(WIDTH//2, 200))

        self.youWonSurf = self.startMenu.mediumFont.render('YOU WON!', True, 'white')
        self.youWonRect = self.youWonSurf.get_rect(center=(WIDTH//2, 250))

        self.wonSpriteSurf = pg.transform.scale(self.player.image, (300, 300))
        self.wonSpriteRect = self.wonSpriteSurf.get_rect(center=(WIDTH//2, HEIGHT//2+100))

    def drawMap(self):
        layouts = {
            BOUNDARY: getLayout('map\\map_FloorBlocks.csv'),
            GRASS: getLayout('map\\map_Grass.csv'),
            OBJECT: getLayout('map\\map_Objects.csv'),
            ENTITIES: getLayout('map\\map_Entities.csv')
        }

        graphics = {
            GRASS: getFolder('graphics\\grass'),
            OBJECT: getFolder('graphics\\objects')
        }

        for type, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, element in enumerate(row):
                    if element != '-1':
                        x = j * TILESIZE
                        y = i * TILESIZE

                        if type == BOUNDARY: Tile((x, y),
                                                  (self.obstacleSprites,),
                                                  INVISIBLE)

                        if type == GRASS: Tile((x, y),
                                               (self.visibleSprites, self.obstacleSprites, self.attackableSprites),
                                               GRASS,
                                               choice(graphics[GRASS]))

                        if type == OBJECT: Tile((x, y),
                                                (self.visibleSprites, self.obstacleSprites),
                                                OBJECT,
                                                graphics[OBJECT][int(element)])

                        if type == ENTITIES:
                            match element:
                                case '390':
                                    monsterType = 'bamboo'
                                case '391':
                                    monsterType = 'spirit'
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

    def createWeapon(self): self.currentWeapon = Weapon((self.visibleSprites, self.attackSprites), self.player)

    def toggleUpgradeMenu(self): self.gamePaused = not self.gamePaused

    def createMagic(self, style: str, strength: int, cost: int):
        if style == HEAL: self.magicPlayer.heal(strength, cost, (self.visibleSprites,))
        if style == FLAME: self.magicPlayer.flame(cost, (self.visibleSprites, self.attackSprites))

    def destroyWeapon(self):
        if self.currentWeapon: self.currentWeapon.kill()
        self.currentWeapon = None

    def playerAttack(self):
        if self.attackSprites:
            for sprite in self.attackSprites:
                collidingSprites = pg.sprite.spritecollide(sprite, self.attackableSprites, False)

                if collidingSprites:
                    for target in collidingSprites:
                        if target.spriteType == GRASS:
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

    def deathParticles(self, pos, particleType): self.animationPlayer.createParticles(particleType, pos, (self.visibleSprites,))

    def updatePlayerEXP(self, amount: int): self.player.exp += amount

    def displayScore(self):
        scoreSurf = self.font.render(f'SCORE: {abs(int(self.player.score))}', True, 'white')
        pg.draw.rect(self.display, 'black', (1125, 15, 150, 23))
        self.display.blit(scoreSurf, (1130, 14))

    def dayNightFunc(self):
        time = pg.time.get_ticks()
        # self.dayNum = time//20000  # every 20 secs
        self.dayNum = time//10000  # test

        self.alpha += 0.37
        if self.alpha >= 180: self.alpha = -180

        self.dayNightSurf.set_alpha(abs(self.alpha))
        self.display.blit(self.dayNightSurf, (0, 0))
        debug(int(self.dayNum))

    def gameEndOverlay(self):
        self.startMenu.transparentOverlay.set_alpha(200)
        self.display.blit(self.startMenu.transparentOverlay, (0, 0))
        self.display.blit(self.startMenu.exitButtonSurf, self.startMenu.exitButtonRect)
        self.display.blit(self.startMenu.muteButtonSurf, self.startMenu.muteButtonRect)
        self.display.blit(self.startMenu.muteButtonIconSurf, self.startMenu.muteButtonIconRect)

        self.display.blit(self.player.finalScoreTextSurf, self.player.finalScoreTextRect)

        finalScoreSurf = self.player.font.render(str(abs(self.player.score)), True, 'white')
        finalScoreRect = finalScoreSurf.get_rect(center=(180, 430))

        self.display.blit(finalScoreSurf, finalScoreRect)

        self.display.blit(self.startMenu.userNameSurf, self.startMenu.userNameRect.move(0, 100))
        self.display.blit(self.startMenu.highScoreSurf, self.startMenu.highScoreRect.move(0, 100))

    def endGameFunc(self):
        self.gameEndOverlay()
        if self.player.score > self.highscore: self.highscore = self.player.score
        self.gameWon = True
        self.inGame = self.inStartMenu = self.inGameStart = self.gamePaused = False
        self.display.blit(self.startMenu.gameNameSurf, self.startMenu.gameNameRect)
        self.display.blit(self.youWonSurf, self.youWonRect)
        self.display.blit(self.wonSpriteSurf, self.wonSpriteRect)

    def playerDeath(self):
        self.gameEndOverlay()
        self.display.blit(self.deadPlayerSurf, self.deadPlayerRect)
        self.display.blit(self.gameOverSurf, self.gameOverRect)
        self.display.blit(self.youDiedSurf, self.youDiedRect)

    def loginFunc(self):
        self.loggedIn = self.inStartMenu = self.inGameStart = True
        self.startMenu.setUser(self.game.username)
        print(self.startMenu.user)

    def run(self):
        currVolume = self.startMenu.volume / 100

        self.player.weaponAttackSound.set_volume(currVolume)

        for enemy in self.enemies:
            enemy.hitSound.set_volume(currVolume)
            enemy.deathSound.set_volume(currVolume)
            enemy.attackSound.set_volume(currVolume)

        if self.loggedIn:
            self.visibleSprites.draw(self.player)
            self.ui.display()

            if self.inGameStart:
                self.startMenu.run()

            elif self.gamePaused:
                self.upgrade.display()

            elif self.inGame and self.inSettingsMenu:
                self.inStartMenu = False
                self.startMenu.run()
                self.ui.displaySettingsButton()
                self.displayScore()

            elif self.player.died:
                self.playerDeath()
                self.displayScore()

            elif self.dayNum >= 5:
                self.endGameFunc()

            else:
                self.displayScore()
                self.visibleSprites.update()
                self.visibleSprites.updateEnemy(self.player)
                self.playerAttack()
                self.leavesOverlay.run()

                if self.loggedIn: self.dayNightFunc()

        debug(f'inGame:{self.inGame}, inSettingsMenu: {self.inSettingsMenu}, inGameStart:{self.inGameStart}, inStartMenu:{self.inStartMenu},\
 loggedIn:{self.loggedIn}, user:{self.username}')
