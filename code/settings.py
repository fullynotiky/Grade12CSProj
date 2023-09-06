WIDTH = 1280
HEIGHT = 670

FPS = 60
TILESIZE = 64
ENERGY_RECOVERY_RATE = 0.01
GROUND = 0
ROCK = 1
PLAYER = 2

HORIZONTAL = 3
VERTICAL = 4

BOUNDARY = 5
GRASS = 6
OBJECT = 7
ENTITIES = 8
INVISIBLE = 9

IDLE = 'idle'
ATTACK = 'attack'
UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'
RIGHT_IDLE = 'right_idle'
LEFT_IDLE = 'left_idle'
UP_IDLE = 'up_idle'
DOWN_IDLE = 'down_idle'
RIGHT_ATTACK = 'right_attack'
LEFT_ATTACK = 'left_attack'
UP_ATTACK = 'up_attack'
DOWN_ATTACK = 'down_attack'

HITBOX_OFFSET = {
    PLAYER: -26,
    OBJECT: -100,
    GRASS: -10,
    INVISIBLE: 0
}

SWORD = 'sword'
LANCE = 'lance'
AXE = 'axe'
RAPIER = 'rapier'
SAI = 'sai'

HEALTH = 'health'
SPEED = 'speed'
ENERGY = 'energy'
ENEMY = 13
FLAME = 'flame'
HEAL = 'heal'
MAGIC = 'magic'
MOVE = 'move'

TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = TEXT_COLOR_SELECTED
UPGRADE_BG_COLOR_SELECTED = BAR_COLOR

WEAPON = 'weapon'
WEAPONS = {
    SWORD: {'cooldown': 100,
            'damage': 15,
            'graphic': 'graphics/weapons/sword/full.png'
            },

    LANCE: {'cooldown': 400,
            'damage': 30,
            'graphic': 'graphics/weapons/lance/full.png'
            },

    AXE: {'cooldown': 300,
          'damage': 20,
          'graphic': 'graphics/weapons/axe/full.png'
          },

    RAPIER: {'cooldown': 50,
             'damage': 8,
             'graphic': 'graphics/weapons/rapier/full.png'
             },

    SAI: {'cooldown': 80,
          'damage': 10,
          'graphic': 'graphics/weapons/sai/full.png'
          }
}

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
FONT = 'graphics/font/joystix.ttf'
FONT_SIZE = 25

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

MAGICS = {
    'flame': {'strength': 5,
              'cost': 20,
              'graphic': 'graphics/particles/flame/fire.png'
              },

    'heal': {'strength': 20,
             'cost': 10,
             'graphic': 'graphics/particles/heal/heal.png'
             }
}

ATTACK_TYPE = 'attack_type'

MONSTERS = {
    'squid': {'health': 100,
              'exp': 100,
              'damage': 20,
              'attack_type': 'slash',
              'attack_sound': 'audio/attack/slash.wav',
              'speed': 3,
              'resistance': 3,
              'attack_radius': 80,
              'notice_radius': 360
              },

    'raccoon': {'health': 300,
                'exp': 250,
                'damage': 40,
                'attack_type': 'claw',
                'attack_sound': 'audio/attack/claw.wav',
                'speed': 2,
                'resistance': 3,
                'attack_radius': 120,
                'notice_radius': 400
                },

    'spirit': {'health': 100,
               'exp': 110,
               'damage': 8,
               'attack_type': 'thunder',
               'attack_sound': 'audio/attack/fireball.wav',
               'speed': 4,
               'resistance': 3,
               'attack_radius': 60,
               'notice_radius': 350
               },

    'bamboo': {'health': 70,
               'exp': 120,
               'damage': 6,
               'attack_type': 'leaf_attack',
               'attack_sound': 'audio/attack/slash.wav',
               'speed': 3,
               'resistance': 3,
               'attack_radius': 50,
               'notice_radius': 300
               }
}
