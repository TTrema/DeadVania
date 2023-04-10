LEVEL_MAP = [

'X                          X',
'X                          X',
'X                          X',
'X                          X',
'X                          X',
'X                          X',
'X                          X',
'X                          X',
'X                          X',
'X                          X',
'X                          X',
'X        JJJ               X',
'X                          X',
'X               JJJ    E   X',
'X   JJJ   B                X',
'X                          X',
'X                     P    X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXX']

TILE_SIZE = 32
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS      = 60

# colors 
BG_COLOR = '#060C17'
PLAYER_COLOR = '#C4F7FF'
TILE_COLOR = '#94D7F2'

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = './graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'


# camera
CAMERA_BORDERS = {
	'left': 100,
	'right': 200,
	'top':100,
	'bottom': 150
}

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'./graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'./graphics/particles/heal/heal.png'}}

monster_data = {
	'smallbee': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'fly': True, 'size': 2.5, 'offset': 0,'rect': (0,0), 'attack_sound':'./audio/attack/slash.wav', 'speed': 6, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 500},
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'worm': {'health': 300,'exp':250,'damage':40,'attack_type': 'fireball', 'size': 4, 'offset': 0,'rect': (0,0), 'attack_sound':'./audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 400},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'./audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'./audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'slime': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'size': 4, 'offset': -30, 'rect': (0,0),'attack_sound':'./audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}