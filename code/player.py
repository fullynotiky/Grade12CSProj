from os import chdir

import pygame as pg

from entity import Entity
from settings import *
from utils import *

chdir('E:\\Harshith\\Python Programming\\School Stuff\\School Project')


class Player(Entity):
    def __init__(self,
                 pos: tuple[int, int],
                 groups: pg.sprite.Group,
                 obstacles: pg.sprite.Group,
                 createWeapon,
                 destroyWeapon,
                 createMagic,
                 level) -> None:

        super().__init__(groups)

        self.finalScoreRect = None
        self.finalScoreSurf = None
        self.finalScoreTextRect = None
        self.finalScoreTextSurf = None
        self.died = None
        self.animations = None
        self.won = False
        self.font = pg.font.Font(FONT, FONT_SIZE + 25)
        self.image = pg.image.load('graphics\\test\\player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-25, HITBOX_OFFSET[PLAYER])
        self.level = level

        self.createWeapon = createWeapon
        self.destroyWeapon = destroyWeapon
        self.weaponIndex = 0
        self.weapon = tuple(WEAPONS)[self.weaponIndex]

        self.canChangeWeapon = True
        self.weaponChangeCooldown = 200
        self.weaponSwitchTime = 0
        self.isAttacking = False
        self.attackCooldown = 400  # ms
        self.attackTime = 0

        self.createMagic = createMagic
        self.magicIndex = 0
        self.magic = tuple(MAGICS)[self.magicIndex]
        self.canChangeMagic = True
        self.magicSwitchTime = 0

        self.state = DOWN
        self.obstacles = obstacles

        self.stats = {
            HEALTH: 100,
            ENERGY: 60,
            SPEED: 7,
            ATTACK: 10,
            MAGIC: 5
        }
        self.maxStats = {
            HEALTH: 300,
            ENERGY: 140,
            SPEED: 15,
            ATTACK: 20,
            MAGIC: 10
        }
        self.upgradeCosts = {
            HEALTH: 90,
            ENERGY: 80,
            SPEED: 100,
            ATTACK: 110,
            MAGIC: 150
        }

        self.speed = self.stats[SPEED]
        self.health = self.stats[HEALTH]
        self.health = 400
        self.energy = self.stats[ENERGY]
        self.exp = 3000
        self.inExp = 3000
        self.score = self.inExp - self.exp

        self.importAssets()

        self.isVulnerable = True
        self.damageTime = 0
        self.invincibilityPeriod = 500

        self.weaponAttackSound = pg.mixer.Sound('audio\\sword.wav')
        self.weaponAttackSound.set_volume(0.4)

        self.finalScoreTextSurf = self.font.render('Your score:', True, 'white')
        self.finalScoreTextRect = self.finalScoreTextSurf.get_rect(topleft=(40, 370))

    def input(self):
        if not self.isAttacking:
            keys = pg.key.get_pressed()

            if keys[pg.K_w]:
                self.state = UP
                self.direction.y = -1
            elif keys[pg.K_s]:
                self.state = DOWN
                self.direction.y = 1
            else:
                self.direction.y = 0

            if keys[pg.K_d]:
                self.state = RIGHT
                self.direction.x = 1
            elif keys[pg.K_a]:
                self.state = LEFT
                self.direction.x = -1
            else:
                self.direction.x = 0

            if keys[pg.K_SPACE]:
                self.isAttacking = True
                self.attackTime = pg.time.get_ticks()
                self.createWeapon()
                self.weaponAttackSound.play()

            if keys[pg.K_RCTRL]:
                self.isAttacking = True
                self.attackTime = pg.time.get_ticks()

                style = tuple(MAGICS)[self.magicIndex]
                strength = tuple(MAGICS.values())[self.magicIndex]['strength'] + self.stats['magic']
                cost = tuple(MAGICS.values())[self.magicIndex]['cost']
                self.createMagic(style, strength, cost)

            if keys[pg.K_q] and self.canChangeWeapon:
                if self.weaponIndex < len(tuple(WEAPONS)) - 1:
                    self.weaponIndex += 1
                else:
                    self.weaponIndex = 0

                self.canChangeWeapon = False
                self.weaponSwitchTime = pg.time.get_ticks()
                self.weapon = tuple(WEAPONS)[self.weaponIndex]

            if keys[pg.K_e] and self.canChangeMagic:
                if self.magicIndex < len(tuple(MAGICS)) - 1:
                    self.magicIndex += 1
                else:
                    self.magicIndex = 0

                self.canChangeMagic = False
                self.magicSwitchTime = pg.time.get_ticks()
                self.magic = tuple(MAGICS)[self.magicIndex]

    def getstate(self):
        if self.direction.x == 0 and self.direction.y == 0 and ATTACK not in self.state:
            if IDLE not in self.state:
                self.state += '_' + IDLE

        if self.isAttacking:
            self.direction.x = self.direction.y = 0
            if ATTACK not in self.state:
                if IDLE in self.state:
                    self.state = self.state.replace('_' + IDLE, '_' + ATTACK)
                else:
                    self.state += '_' + ATTACK

        else:
            if ATTACK in self.state: self.state = self.state.replace('_' + ATTACK, '')

    def getTotalWeaponDamage(self): return self.stats[ATTACK] + WEAPONS[self.weapon]['damage']

    def getTotalMagicDamage(self): return self.stats[MAGIC] + MAGICS[self.magic]['strength']

    def importAssets(self):
        subPath = 'graphics\\player\\'

        self.animations = {
            UP: [],
            DOWN: [],
            LEFT: [],
            RIGHT: [],
            LEFT_IDLE: [],
            RIGHT_IDLE: [],
            UP_IDLE: [],
            DOWN_IDLE: [],
            RIGHT_ATTACK: [],
            LEFT_ATTACK: [],
            UP_ATTACK: [],
            DOWN_ATTACK: [],
        }

        for animation in self.animations: self.animations[animation] = getFolder(subPath + animation)

    def move(self, speed: int):
        if self.direction.magnitude(): self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision(HORIZONTAL)

        self.hitbox.y += self.direction.y * speed
        self.collision(VERTICAL)

        self.rect.center = self.hitbox.center

    def cooldowns(self):
        currTime = pg.time.get_ticks()

        if self.isAttacking:
            if currTime - self.attackTime >= self.attackCooldown + WEAPONS[self.weapon]['cooldown']:
                self.isAttacking = False
                self.destroyWeapon()

        if not self.canChangeWeapon:
            if currTime - self.weaponSwitchTime >= self.weaponChangeCooldown:
                self.canChangeWeapon = True

        if not self.canChangeMagic:
            if currTime - self.magicSwitchTime >= self.weaponChangeCooldown:
                self.canChangeMagic = True

        if not self.isVulnerable:
            if currTime - self.damageTime >= self.invincibilityPeriod:
                self.isVulnerable = True

    def collision(self, direction):
        if direction == HORIZONTAL:
            for sprite in self.obstacles:

                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.rect.left

                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.rect.right

        elif direction == VERTICAL:
            for sprite in self.obstacles:

                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.rect.top

                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.rect.bottom

    def animate(self):
        animation = self.animations[self.state]

        self.frameIndex += self.animationSpeed
        if self.frameIndex > len(animation): self.frameIndex = 0

        self.image = animation[int(self.frameIndex)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.isVulnerable: self.image.set_alpha(self.getFlickerValue())
        else: self.image.set_alpha(255)

    def energyRegen(self):
        if self.energy < self.stats[ENERGY]: self.energy += ENERGY_RECOVERY_RATE * self.stats[MAGIC]
        else: self.energy = self.stats[ENERGY]

    def deathFunc(self):
        self.died = True
        self.level.inGame = self.level.inGameStart = self.level.inStartMenu = self.level.inSettingsMenu = False
        self.finalScoreSurf = self.font.render(str(abs(self.score)), True, 'white')
        self.finalScoreRect = self.finalScoreSurf.get_rect(center=(180, 430))
        
    def update(self):
        self.score = self.inExp - self.exp
        self.input()
        self.cooldowns()
        self.getstate()
        self.animate()
        self.energyRegen()
        self.move(self.speed)
        self.checkDeath(self.deathFunc)
