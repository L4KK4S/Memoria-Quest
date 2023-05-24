""" Projet Transverse - Groupe A3 - Fichier main.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Python libraries
import pygame

# Internal modules
import variables as v
import constants as c
import maps as Maps
from ui import GraphUI
from ux import GameUX
from structure import Struct


# ___________________________________________ CLASSES ____________________________________________ #


class Main:
    """ Main class of the game """

    # -------------------------------------------------------------------------------------------- #

    def __init__(self) -> None:
        """ Init Pygame window """
        pygame.init()
        v.W = pygame.display.Info().current_w+2  # use full desktop width
        v.H = pygame.display.Info().current_h+2  # use full desktop height
        v.screen = pygame.display.set_mode((v.W, v.H), pygame.NOFRAME)  # game screenF
        pygame.display.set_caption(c.GAME_NAME)  # game caption
        pygame.display.set_icon(pygame.image.load(c.GAME_ICON_FILE_PATH))  # game icon

    # -------------------------------------------------------------------------------------------- #

    def run_game(self) -> None:
        """ Main game loop """
        v.clock = pygame.time.Clock()
        v.keys_pressed = pygame.key.get_pressed()
        v.MousePos.end_motion = c.DEF_POS
        pygame.key.set_repeat(1, 5)
        pygame.mouse.set_visible(0)
        v.temp_tick = 0

        GameUX.set_sounds()
        GameUX.start_music(v.MusicPaths['menu_music'])

        # Background gif images
        for i in range(c.NB_IMG_BG_GIF):
            v.images_to_load[f'gif_menu_frame_{i}'] = (f'backgrounds/forest/gif/frame ({i+1}).gif',
                                                       (v.W, v.H))

        # Background game images
        for i in range(3):
            for j in range(3):
                v.images_to_load[f'map{i+1}_bg{j+1}'] = (f'backgrounds/map{i+1}/bg{j+1}.png',
                                                         (v.W, v.H))
                v.images_to_load[f'map{i+1}_bg{j+1}_lil'] = (f'backgrounds/map{i+1}/bg{j+1}.png',
                                                             (350, 250))

        v.level = Maps.MapHandler()
        v.camera = Maps.Camera(v.level)

        Struct.loading_loop()

        if v.running:
            v.tours = 0

        while v.running:
            v.MousePos.click_down = c.DEF_POS
            v.MousePos.click_up = c.DEF_POS
            GameUX.handle_events()
            v.last_subpage = v.subpage
            v.mouse.update_position()
            v.screen.fill(c.DARK_SLATE_GRAY)

            # Call page functions
            if v.subpage in dir(Struct):
                exec(f'Struct.{v.subpage}()')
            else:
                Struct.unknown_page()
            if v.confirm_quit:
                Struct.confirm_quit()
            elif v.confirm_back_to_menu:
                Struct.confirm_back_to_menu()

            GameUX.egg()
            GameUX.debug_messages()

            # Handle cursors
            if v.page == 'menu' or v.confirm_quit or (v.page == 'game' and v.subpage != 'game_arcade'):
                GraphUI.ImageBox('cursor', v.mouse.rect.x - v.camera.scroll_x,
                                 v.mouse.rect.y - v.camera.scroll_y, 'TL')

            v.clock.tick(v.FPS)
            pygame.display.update()
            v.tours += 1

        pygame.quit()

# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
