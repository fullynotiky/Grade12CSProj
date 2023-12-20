from os import chdir

import pygame as pg

from entity import Entity
from globals import *
from utils import *


class Player(Entity):
    def __init__(self,
                 pos: tuple[int, int],
                 groups: pg.sprite.Group,
                 obstacles: pg.sprite.Group,
                 createWeapon,
                 destroyWeapon,
                 createMagic,
                 level):

        super().__init__(groups)
        
        self.finalScoreRect = self.finalScoreSurf = self.animations = None
        self.won = self.died = False
        self.font = pg.font.Font(FONT_PATH, FONT_SIZE + 25)
        self.image = pg.image.load('graphics\\test\\player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-25, HITBOX_OFFSET['player'])
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
        self.magic = tuple(SPELLS)[self.magicIndex]
        self.canChangeMagic = True
        self.magicSwitchTime = 0

        self.state = 'down'
        self.obstacles = obstacles

        self.stats = {
            'health': 100,
            'energy': 60,
            'speed': 7,
            'attack': 10,
            'spell': 5
        }
        self.maxStats = {
            'health': 300,
            'energy': 140,
            'speed': 15,
            'attack': 20,
            'spell': 10
        }
        self.upgradeCosts = {
            'health': 90,
            'energy': 80,
            'speed': 100,
            'attack': 110,
            'spell': 150
        }

        self.speed = self.stats['speed']
        self.health = self.stats['health']
        self.health = 300
        self.energy = self.stats['energy']
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

            if keys[pg.K_w]: self.state, self.direction.y = 'up', -1
            elif keys[pg.K_s]: self.state, self.direction.y = 'down', 1
            else: self.direction.y = 0

            if keys[pg.K_d]: self.state, self.direction.x = 'right', 1
            elif keys[pg.K_a]: self.state, self.direction.x = 'left', -1
            else: self.direction.x = 0

            if keys[pg.K_SPACE]:
                self.isAttacking = True
                self.attackTime = pg.time.get_ticks()
                self.createWeapon()
                self.weaponAttackSound.play()

            if keys[pg.K_RCTRL]:
                self.isAttacking = True
                self.attackTime = pg.time.get_ticks()

                style = tuple(SPELLS)[self.magicIndex]
                strength = tuple(SPELLS.values())[self.magicIndex]['strength'] + self.stats['spell']
                cost = tuple(SPELLS.values())[self.magicIndex]['cost']
                self.createMagic(style, strength, cost)

            if keys[pg.K_q] and self.canChangeWeapon:
                if self.weaponIndex < len(tuple(WEAPONS)) - 1: self.weaponIndex += 1
                else: self.weaponIndex = 0

                self.canChangeWeapon = False
                self.weaponSwitchTime = pg.time.get_ticks()
                self.weapon = tuple(WEAPONS)[self.weaponIndex]

            if keys[pg.K_e] and self.canChangeMagic:
                if self.magicIndex < len(tuple(SPELLS)) - 1: self.magicIndex += 1
                else: self.magicIndex = 0

                self.canChangeMagic = False
                self.magicSwitchTime = pg.time.get_ticks()
                self.magic = tuple(SPELLS)[self.magicIndex]

    def getstate(self):
        if self.direction.x == 0 and self.direction.y == 0 and 'attack' not in self.state:
            if 'idle' not in self.state: self.state += '_' + 'idle'

        if self.isAttacking:
            self.direction.x = self.direction.y = 0
            if 'attack' not in self.state:
                if 'idle' in self.state: self.state = self.state.replace('_' + 'idle', '_' + 'attack')
                else: self.state += '_' + 'attack'

        else:
            if 'attack' in self.state: self.state = self.state.replace('_' + 'attack', '')

    def getTotalWeaponDamage(self): return self.stats['attack'] + WEAPONS[self.weapon]['damage']

    def getTotalSpellDamage(self): return self.stats['spell'] + SPELLS[self.magic]['strength']

    def importAssets(self):
        subPath = 'graphics\\player\\'

        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'left_idle': [],
            'right_idle': [],
            'up_idle': [],
            'down_idle': [],
            'right_attack': [],
            'left_attack': [],
            'up_attack': [],
            'down_attack': [],
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

        if not self.canChangeWeapon and (currTime - self.weaponSwitchTime >= self.weaponChangeCooldown): self.canChangeWeapon = True
        if not self.canChangeMagic and (currTime - self.magicSwitchTime >= self.weaponChangeCooldown): self.canChangeMagic = True
        if not self.isVulnerable and (currTime - self.damageTime >= self.invincibilityPeriod): self.isVulnerable = True

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
        if self.energy < self.stats['energy']: self.energy += ENERGY_RECOVERY_RATE * self.stats['spell']
        else: self.energy = self.stats['energy']

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
