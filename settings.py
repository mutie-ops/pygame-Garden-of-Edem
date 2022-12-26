WIDTH = 1280
HEIGHT = 720
FPS = 60

LAYERS = {'ground': 0,
          'hills': 1,
          'ground_plants': 2,
          'main': 3}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'C:\\Users\\benja\\Desktop\\pythonProject\\tiles\\fonts\\STIXGeneral.ttf'
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

# weapons/tools
tool_data = {'staff': {'cooldown': 100, 'damage': 15,
                       'graphics': 'C:\\Users\\benja\\Desktop\\pythonProject\\tiles\\weapon\\staff.png'},
             'sword': {'cooldown': 100, 'damage': 5,
                       'graphics': 'C:\\Users\\benja\\Desktop\\pythonProject\\tiles\\weapon\\sword.png'}}
# magic
magic_data = {'die': {'strength': 100, 'cost': 100,
                      'graphics': 'C:\\Users\\benja\\Desktop\\pythonProject\\tiles\\magic\\wither.png'},
              'flame': {'strength': 50, 'cost': 10,
                        'graphics': 'C:\\Users\\benja\\Desktop\\pythonProject\\tiles\\magic\\fire.png'},
              'heal': {'strength': 15, 'cost': 15,
                       'graphics': 'C:\\Users\\benja\\Desktop\\pythonProject\\tiles\\magic\\heal.png'},
              }

# monsters

monster_data = {
    'goblin_general': {'health': 200, 'exp': 100, 'damage': 5, 'attack_type': 'slash', 'speed': 1.5, 'resistance': 3,
                       'attack_radius': 80, 'notice_radius': 360}}

# Vosk model
voice_model = 'C:\\Users\\benja\\Desktop\\pythonProject\\adam\\vosk-model-en-us-0.22'
