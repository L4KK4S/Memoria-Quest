""" Projet Transverse - Groupe A3 - Fichier constants.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Python libraries
import pygame


# __________________________________________ CONSTANTS ___________________________________________ #


GAME_NAME = 'MEMORIA QUEST'
GAME_ICON_FILE_PATH = '../assets/img/icons/game_logo.ico'

MAX_PLAYERS = 4
NB_IMG_BG_GIF = 1  # max 300

BG_GIF_FPS = 15  # can't be higher than FPS

TILE_SIZE = 32
GRAVITY = 9.8

COMMANDS = {'jump': pygame.K_SPACE,
            'down': pygame.K_s,
            'arrow path': pygame.K_e,
            'shoot': pygame.K_a,
            'attack': pygame.K_i,
            'dash': pygame.K_v,
            'viewfinder_up': pygame.K_o,
            'viewfinder_down': pygame.K_l,
            'viewfinder_left': pygame.K_k,
            'viewfinder_right': pygame.K_m,
            'left': pygame.K_q,
            'right': pygame.K_d,
            'death': pygame.K_1,  # death et hit pour tester les animations
            'hit': pygame.K_2}

DEF_FALSE = [False, False, False]
DEF_POS = (-10, -10)

# ------------------------------------------------------------------------------------------------ #

# Basic colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 0, 0)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)

# Colors and palettes found from https://coolors.co/generate
DARK_SLATE_GRAY = (53, 82, 74)
LIGHT_SLATE_GRAY = (119, 136, 153)
SLATE_GRAY = (96, 129, 136)
LIGHT_GRAY = (211, 211, 211)
LIGHT_STEEL_BLUE = (176, 196, 222)
DIM_GRAY = (105, 105, 105)
SILVER = (193, 193, 193)
PALE_DOGWOOD = (244, 214, 204)
BRIGHT_PINK = (255, 69, 108)
LAVENDER_BLUSH = (255, 236, 240)
GUNMETAL = (21, 34, 39)
PAKISTAN_GREEN = (33, 51, 20)
COLOR_P1 = (64, 131, 198)
COLOR_P2 = (75, 103, 54)
COLOR_P3 = (186, 94, 94)
COLOR_P4 = (101, 50, 149)
ASH_GRAY = (164, 186, 183)
CAMBRIDGE_BLUE = (116, 145, 141)
AMARANTH_PURPLE = (164, 48, 63)
FELDGRAU = (64, 99, 89)
MYRTLE_GREEN = (84, 130, 132)
CADET_GRAY = (137, 174, 176)
MOONSTONE = (101, 134, 135)
SLIDER_OVER = (0, 180, 216)
SLIDER_UNDER = (0, 59, 71)
SLIDER_BUTTON = (238, 229, 233)

# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
