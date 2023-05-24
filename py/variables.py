""" Projet Transverse - Groupe A3 - Fichier variables.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Python libraries
import os
import json

# Internal modules
import constants as c


# __________________________________________ VARIABLES ___________________________________________ #

# Mouse, click, keys, active events


class MousePos:
    end_motion = c.DEF_POS
    click_down = c.DEF_POS
    click_up = c.DEF_POS


keys_pressed = []
oob_ctrl = False  # one or both CTRL keys pressed
oob_shift = False  # one or both SHIFT keys pressed

# event_id that we need to create before first execution
events_id_list = ['play', 'options', 'quit', 'return', 'yes_quit', 'no_stay',
                  'menu_arcade', 'start', 'resume', 'main_menu', 'break_btn',
                  'char1', 'char2', 'char3', 'char4', 'map1', 'map2', 'map3',
                  'next', 'nb1', 'nb2', 'nb3', 'nb4', 'slider_lives',
                  'slider_sound', 'slider_music', 'leaderboard', 'sort_score',
                  'sort_player', 'sort_date', 'btm_yes', 'btm_no', 'hardcore',
                  'left_arrow', 'right_arrow', 'fps_onoff',
                  'name1', 'name2', 'name3', 'name4', 'random_name1',
                  'random_name2', 'random_name3', 'random_name4']
Events = {i: c.DEF_FALSE for i in events_id_list}  # [end_motion/hover, click_up, click_down]
Active = {i: False for i in events_id_list}  # [active]

# ------------------------------------------------------------------------------------------------ #

# Sounds

SoundsPath = {'click': '../assets/audio/click.wav',
              'hover': '../assets/audio/hover.wav',
              'bonus': '../assets/audio/bonus.wav',
              'smash': '../assets/audio/smash.wav',
              'kill': '../assets/audio/kill.wav'}
Sounds = {i: None for i in SoundsPath}
sound_volume = 1

MusicPaths = {'menu_music': '../assets/audio/menu_music.mp3',
              'game_music': '../assets/audio/game_music.mp3'}
Music = {i: None for i in MusicPaths}
music_volume = 0.4

# ------------------------------------------------------------------------------------------------ #

# Images

images_dir = '../assets/img/'
images_to_load = {'cursor': ('icons/cursor.png', (32,)),
                  'wood_button': ('buttons/simple_button/dark_wood_button.png', (300,)),
                  'wood_button_hover': ('buttons/simple_button/light_wood_button.png', (300,)),
                  'wood_lil_button': ('buttons/simple_button/dark_wood_button.png', (150,)),
                  'wood_lil_button_hover': ('buttons/simple_button/light_wood_button.png', (150,)),
                  'switch_button_1': ('buttons/switch_button/frame1.png', (120,)),
                  'switch_button_2': ('buttons/switch_button/frame2.png', (120,)),
                  'switch_button_3': ('buttons/switch_button/frame3.png', (120,)),
                  'switch_button_4': ('buttons/switch_button/frame4.png', (120,)),
                  'egg0': ('icons/egg0.png', (400,)),
                  'python': ('icons/python.png', (100,)),
                  'title': ('icons/game_title.png', (1000,)),
                  'bringer-of-death': ('enemies/Bringer-of-Death.png', (98,)),
                  'viewfinder': ('icons/viseur.png', (32,)),
                  'arrow': ('player/arrow.png', (20,)),
                  'cup': ('icons/cup.png', (70,)),
                  'cup_hover': ('icons/cup.png', (75,)),
                  'sort_asc': ('icons/sort_asc.png', (30,)),
                  'sort_asc_hover': ('icons/sort_asc.png', (35,)),
                  'sort_desc': ('icons/sort_desc.png', (30,)),
                  'sort_desc_hover': ('icons/sort_desc.png', (35,)),
                  'first': ('icons/first.png', (35,)),
                  'second': ('icons/second.png', (35,)),
                  'third': ('icons/third.png', (35,)),
                  'left_arrow': ('icons/left_arrow.png', (50,)),
                  'right_arrow': ('icons/right_arrow.png', (50,)),
                  'left_arrow_hover': ('icons/left_arrow.png', (60,)),
                  'right_arrow_hover': ('icons/right_arrow.png', (60,)),
                  'left_arrow_black': ('icons/left_arrow_black.png', (40,)),
                  'right_arrow_black': ('icons/right_arrow_black.png', (40,)),
                  'left_arrow_silver': ('icons/left_arrow_silver.png', (40,)),
                  'right_arrow_silver': ('icons/right_arrow_silver.png', (40,)),
                  'left_arrow_dim_gray': ('icons/left_arrow_dim_gray.png', (40,)),
                  'right_arrow_dim_gray': ('icons/right_arrow_dim_gray.png', (40,)),
                  'left_arrow_black_hover': ('icons/left_arrow_black.png', (50,)),
                  'right_arrow_black_hover': ('icons/right_arrow_black.png', (50,)),
                  'eye': ('enemies/eye.png', (32,)),
                  'heart': ('player/heart.png', (48,)),
                  'half_heart': ('player/half_heart.png', (48,)),
                  'skull': ('player/skull.png', (48,)),
                  'life_potion': ('bonus/life_potion.png', (24,)),
                  'speed_potion': ('bonus/speed_potion.png', (24,)),
                  'power_potion': ('bonus/power_potion.png', (24,)),
                  'random': ('icons/random.png', (50,)),
                  'random_hover': ('icons/random.png', (60,))}


# Lists all the frames of the player and load them
for folder in os.listdir(images_dir+'player/'):
    if not os.path.isfile(images_dir+'player/'+folder):
        frames = os.listdir(images_dir+'player/'+folder)
        for i in range(len(frames)):
            images_to_load[f'player_{folder}_{i+1}'] = (f'player/{folder}/{frames[i]}',
                                                        (79*2, 43*2))

# Puts all tiles of all maps in the dictionary
for tile in os.listdir(images_dir+'tileset/'):
    images_to_load[f'map_{tile[:-4]}'] = (f'tileset/{tile}', (32,))

# frames of Bringer of Death
for folder in os.listdir(images_dir+'enemies/Bringer_of_death/'):
    frames = os.listdir(images_dir+'enemies/Bringer_of_death/'+folder)
    for i in range(len(frames)):
        images_to_load[f'Bringer-of-Death_{folder}_{i+1}'] = (f'enemies/Bringer_of_death/{folder}/{frames[i]}', (185*1.5, 85*1.5))

# frames of Goblin
for folder in os.listdir(images_dir+'enemies/Goblin/'):
    frames = os.listdir(images_dir+'enemies/Goblin/'+folder)
    for i in range(len(frames)):
        images_to_load[f'Goblin_{folder}_{i+1}'] = (f'enemies/Goblin/{folder}/{frames[i]}', (90, 55))

# frames of Boar
for folder in os.listdir(images_dir+'enemies/Boar/'):
    frames = os.listdir(images_dir+'enemies/Boar/'+folder)
    for i in range(len(frames)):
        images_to_load[f'Boar_{folder}_{i+1}'] = (f'enemies/Boar/{folder}/{frames[i]}', (140, 80))

Images = {}

# ------------------------------------------------------------------------------------------------ #

# Fonts

default_font = 'default2'
Fonts = {'default': '../assets/fonts/jmh_beda.ttf',
         'default2': '../assets/fonts/medieval_sharp.ttf',
         'title': '../assets/fonts/bm_army.ttf'}

# ------------------------------------------------------------------------------------------------ #

# Main menu
FPS = 60
running = True
page = 'menu'
subpage = 'home'

confirm_quit = False
confirm_back_to_menu = False
escape_time = 0

countdown = False
countdown_time = 0
countdown_state = 3
countdown_from_break = False

show_fps = False

# Maps
with open('../data/maps.json', 'r') as f:
    Maps = json.loads(f.read())

# Easter eggs
egg = [False]*5
egg_start = [0]*5

# Other
id_players = [-2, -2, -2, -2]
bg_gif_idc = 0
actions_players = [[], [], [], []]
options_from_break = False
options_from_game = False
nb_lives = 5
random_enemies_spawn = 500
random_bonus_spawn = FPS * 5
verif_random = 0
potion_coordinates = {'life_potion': [-1, -1], 'speed_potion': [-1, -1], 'power_potion': [-1, -1]}

# Menu player
nb_player = 0
nb_enemies = 0
nb_bonus = 0

# Menu characters
nb_char_chosen = 0
all_chosen = False
associated_names = {'char1': 'Blue', 'char2': 'Green',
                    'char3': 'Red', 'char4': 'Purple'}
player_choices = {f'P{i+1}': None for i in range(4)}
colors = {'Blue': c.COLOR_P1, 'Green': c.COLOR_P2,
          'Red': c.COLOR_P3, 'Purple': c.COLOR_P4}

player_names = {f'P{i+1}': '' for i in range(4)}

field_focus = None
id_focus = None
nb_fields = 0
tab_time = 0
field_enter = False
field_enter_time = 0
text_input = False
text = ''
text_time = 0
text_overflow = False
text_not_added = False

# Menu maps
map_choice = None

# Options
slider_move = None
SliderPos = {'slider_sound': sound_volume,
             'slider_music': music_volume}

# Leaderboard
to_sort = True
with open('../data/leaderboard.json', 'r') as f:
    Leaderboard = json.loads(f.read())
LeaderboardSorted = {}
Filters = {'sort_score': 'asc',
           'sort_player': 'asc',
           'sort_date': 'asc'}
filter_ = ('sort_score', 'desc')
Top3 = {}
Top3_names = []

escape = False

subpages_list = ['home', 'menu_arcade_choice_nb_players', 'menu_arcade_controllers',
                 'menu_arcade_choice_characters', 'menu_arcade_choice_map', 'break_', 'endgame',
                 'options', 'keys_mod']

# event_id in focus order of all subpages buttons
focus_order = {'home': ['play', 'options', 'quit', 'leaderboard'],
               'menu_arcade_choice_nb_players': ['return', 'nb1', 'nb2', 'nb3', 'nb4', 'next'],
               'menu_arcade_controllers': ['return', 'next'],
               'menu_arcade_choice_characters': ['return', 'char1', 'char2',
                                                 'char3', 'char4'],
               'menu_arcade_choice_map': ['return', 'map1', 'map2', 'map3', 'next'],
               'break_': ['resume', 'options', 'main_menu'],
               'endgame': ['main_menu', 'quit'],
               'options': ['return'],
               'leaderboard': ['return'],
               'confirm_quit': ['yes', 'no'],
               'menu_arcade_options': ['return', 'next'],
               'keys_mod': []}

focus = None
focus_enter = False
on_focus_move = False
last_subpage = subpage

on_off_range = 4
# 'event_id': [start_pos, current_pos]
OnOff = {'hardcore': [0, 0],
         'fps_onoff': [0, 0]}
on_off_transition = {i: 0 for i in list(OnOff)}

wait_for_next_click = False
wait_time = 0

hardcore = False
fps_time = 0

# Value slider
ValueSlider = {'fps': [1, [30, 60, 75, 120, 144, 240]],
               'slider_lives': [0, [3, 4, 5, 6, 7, 8, 9, 10]]}

nb_controllers = 0

game_chrono = 0
start_game_session = 0
stop_game_session = 0

maps_text_color = {'map1': c.WHITE, 'map2': c.BLACK, 'map3': c.BLACK}

RandomNames = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Rep', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Congo {Democratic Rep}', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland {Republic}', 'Palestine', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea North', 'Korea South', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar, {Burma}', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russian Federation', 'Rwanda', 'St Kitts & Nevis', 'St Lucia', 'Saint Vincent & the Grenadines', 'Samoa', 'San Marino', 'Sao Tome & Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad & Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']

# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
