from utils import getJsonFile

WIDTH = 1280
HEIGHT = 670

FPS = 60
TILESIZE = 64
ENERGY_RECOVERY_RATE = 0.01

HORIZONTAL = 3
VERTICAL = 4

TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = TEXT_COLOR_SELECTED
UPGRADE_BG_COLOR_SELECTED = BAR_COLOR

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
FONT_PATH = 'graphics/font/joystix.ttf'
FONT_SIZE = 25

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

SPELLS = getJsonFile('databases\\spells.json')
WEAPONS = getJsonFile('databases\\weapons.json')
MONSTERS = getJsonFile('databases\\monsters.json')
HITBOX_OFFSET = getJsonFile('databases\\offsets.json')
