import pygame as pg

from entity import Entity
from player import Player
from globals import *
from utils import *


class Enemy(Entity):
    def __init__(self,
                 groups,
                 monsterName: str,
                 pos: tuple[int, int],
                 obstacles,
                 player: Player,
                 damageToPlayer,
                 deathParticles,
                 updatePlayerEXP):

        super().__init__(groups)

        self.deathParticles = deathParticles
        self.updatePlayerEXP = updatePlayerEXP

        self.animation = None
        self.animations = None
        self.monsterName = monsterName
        self.importGraphics()

        self.state = 'idle'
        self.spriteType = 'enemy'
        self.player = player

        self.image = self.animations[self.state][self.frameIndex]
        self.rect: pg.Rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(-10, -10)

        self.obstacles = obstacles

        self.monster = MONSTERS[self.monsterName]
        self.health = self.monster['health']
        self.exp = self.monster['exp']
        self.speed = self.monster['speed']
        self.attackDamage = self.monster['damage']
        self.resistance = self.monster['resistance']
        self.attackRadius = self.monster['attack_radius']
        self.noticeRadius = self.monster['notice_radius']
        self.attackType = self.monster['attack_type']

        self.canAttack = True
        self.attackTime = 0
        self.attackCooldown = 400
        self.damageToPlayer = damageToPlayer

        self.isVulnerable = True
        self.damageTime = 0
        self.invincibilityPeriod = 300

        self.deathSound = pg.mixer.Sound('audio\\death.wav')
        self.hitSound = pg.mixer.Sound('audio\\hit.wav')
        self.attackSound = pg.mixer.Sound(self.monster['attack_sound'])
        self.deathSound.set_volume(0.4)
        self.hitSound.set_volume(0.4)
        self.attackSound.set_volume(0.4)

    def importGraphics(self):
        self.animations = {
            'idle': [],
            'move': [],
            'attack': []
        }

        subPath = f'graphics\\monsters\\{self.monsterName}\\'

        for animation in self.animations: self.animations[animation] = getFolder(subPath + animation)

    def getPlayerPos(self):
        relVec = pg.Vector2(self.player.rect.center) - pg.Vector2(self.rect.center)
        distance = relVec.magnitude()
        direc = relVec.normalize() if distance else pg.Vector2()

        return distance, direc

    def getState(self):
        distance = self.getPlayerPos()[0]

        if distance <= self.attackRadius and self.canAttack:
            if self.state != 'attack': self.frameIndex = 0
            self.state = 'attack'
        elif distance <= self.noticeRadius: self.state = 'move'
        else: self.state = 'idle'

    def actions(self):
        if self.state == 'attack' and self.canAttack:
            self.attackTime = pg.time.get_ticks()
            self.attackSound.play()
            self.damageToPlayer(self.attackDamage, self.attackType)
        elif self.state == 'move': self.direction = self.getPlayerPos()[1]
        else: self.direction = pg.Vector2()

    def damageReaction(self):
        if not self.isVulnerable: self.direction *= - self.resistance

    def getDamage(self, player: Player, attackType: str):
        if self.isVulnerable:
            self.hitSound.play()
            self.direction = self.getPlayerPos()[1]
            if attackType == 'weapon': self.health -= player.getTotalWeaponDamage()
            else: self.health -= self.player.getTotalSpellDamage()

            self.damageTime = pg.time.get_ticks()
            self.isVulnerable = False

    def animate(self):
        self.frameIndex += self.animationSpeed
        self.animation = self.animations[self.state]

        if self.frameIndex >= len(self.animation):
            if self.state == 'attack': self.canAttack = False
            self.frameIndex = 0

        self.image = self.animation[int(self.frameIndex)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.isVulnerable: self.image.set_alpha(self.player.getFlickerValue())
        else: self.image.set_alpha(255)

    def cooldowns(self):
        currTime = pg.time.get_ticks()
        if not self.canAttack and currTime - self.attackTime >= self.attackCooldown: self.canAttack = True
        if not self.isVulnerable and currTime - self.damageTime >= self.invincibilityPeriod: self.isVulnerable = True

    def deathFunc(self):
        self.kill()
        self.deathParticles(self.rect.center, self.monsterName)
        self.updatePlayerEXP(self.exp)
        self.deathSound.play()

    def update(self):
        self.damageReaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.checkDeath(self.deathFunc)

    def enemyUpdate(self):
        self.getState()
        self.actions()
