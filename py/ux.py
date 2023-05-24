""" Projet Transverse - Groupe A3 - Fichier ux.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Python libraries
import pygame

# Internal modules
import variables as v
import constants as c
from ui import GraphUI


# ___________________________________________ CLASSES ____________________________________________ #


class GameUX:

    """ Set of functions managing the user experience """

    # -------------------------------------------------------------------------------------------- #

    def pressed_keys(*keys: int) -> bool:
        """ Returns True if :*keys: pressed at the same time """
        return all(v.keys_pressed[i] for i in keys)

    # -------------------------------------------------------------------------------------------- #

    def handle_events() -> None:
        """ Loop to handle user events """
        v.escape = False
        v.focus_enter = False
        v.field_enter = False
        v.keys_pressed = pygame.key.get_pressed()
        v.oob_ctrl = v.keys_pressed[pygame.K_LCTRL] or v.keys_pressed[pygame.K_RCTRL]
        v.oob_shift = v.keys_pressed[pygame.K_LSHIFT] or v.keys_pressed[pygame.K_RSHIFT]

        if (pygame.time.get_ticks()-v.wait_time)/1000 >= 0.25:
            v.wait_for_next_click = False
            v.wait_time = pygame.time.get_ticks()

        # Events control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                v.confirm_quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN and not v.wait_for_next_click:
                v.MousePos.click_down = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and not v.wait_for_next_click:
                v.MousePos.click_up = event.pos
                v.slider_move = None
            elif event.type == pygame.MOUSEMOTION:
                v.MousePos.end_motion = event.pos
            elif not pygame.mouse.get_focused():
                v.MousePos.end_motion = c.DEF_POS
            elif event.type == pygame.KEYDOWN:
                if v.text_input and (pygame.time.get_ticks()-v.text_time)/1000 >= 0.125:
                    if v.field_focus is not None:
                        if event.unicode.isprintable() and not v.text_overflow:
                            if v.subpage == "menu_arcade_choice_names":
                                v.player_names[f'P{v.field_focus+1}'] += event.unicode
                        elif event.key == pygame.K_BACKSPACE:
                            w = v.player_names[f'P{v.field_focus+1}'][:-1]
                            v.player_names[f'P{v.field_focus+1}'] = w
                    v.text_time = pygame.time.get_ticks()
            elif event.type == pygame.KEYUP:
                v.on_focus_move = False

        # Keys control
        if v.keys_pressed[pygame.K_ESCAPE]:
            if (pygame.time.get_ticks()-v.escape_time)/1000 >= 0.25:
                v.escape = True
                v.escape_time = pygame.time.get_ticks()
        elif v.keys_pressed[pygame.K_RETURN]:
            if (pygame.time.get_ticks()-v.temp_tick)/1000 >= 1:
                v.focus_enter = True
                v.temp_tick = pygame.time.get_ticks()
                if v.confirm_quit:
                    v.running = False
                    v.focus_enter = False
                if v.confirm_back_to_menu:
                    v.page = 'menu'
                    v.subpage = 'home'
                    v.confirm_back_to_menu = False
                    GameUX.stop_music()
                    GameUX.start_music(v.MusicPaths['menu_music'])
                    v.wait_for_next_click = True
                    v.focus_enter = False
            if (pygame.time.get_ticks()-v.field_enter_time)/1000 >= 0.15:
                v.field_enter = True
                v.field_enter_time = pygame.time.get_ticks()
        elif v.oob_ctrl:
            if v.keys_pressed[pygame.K_a]:
                GameUX.egg_control(0)
            if v.subpage == 'game_arcade' and v.keys_pressed[pygame.K_w]:
                v.subpage = 'endgame'
        elif v.keys_pressed[pygame.K_F11] and (pygame.time.get_ticks()-v.fps_time)/1000 >= 0.25:
            v.show_fps = not v.show_fps
            v.fps_time = pygame.time.get_ticks()
        elif v.keys_pressed[pygame.K_TAB] and v.subpage == 'menu_arcade_choice_names':
            if (pygame.time.get_ticks()-v.tab_time)/1000 >= 0.15:
                if v.keys_pressed[pygame.K_LSHIFT]:
                    if v.field_focus is None:
                        v.field_focus = v.nb_fields-1
                    else:
                        v.field_focus -= 1
                    if v.field_focus < 0:
                        v.field_focus = v.nb_fields-1
                else:
                    if v.field_focus is None:
                        v.field_focus = 0
                    else:
                        v.field_focus += 1
                    if v.field_focus > v.nb_fields-1:
                        v.field_focus = 0
                for i in range(v.nb_fields):
                    v.Active[f'name{i+1}'] = (i == v.field_focus)
                v.text_input = False
                v.text_overflow = False
                v.tab_time = pygame.time.get_ticks()

        # Escape control
        if v.escape:
            if v.oob_shift:
                v.running = False
            else:
                if v.confirm_quit:
                    v.confirm_quit = False
                    v.escape = False
                if v.confirm_back_to_menu:
                    v.confirm_back_to_menu = False

        # Focus control
        if v.last_subpage != v.subpage:
            v.focus = None
        if not v.on_focus_move:
            if v.keys_pressed[pygame.K_LEFT]:
                if v.focus is not None:
                    v.focus -= 1
                elif v.subpage in v.focus_order:
                    v.focus = len(v.focus_order[v.subpage])-1
            elif v.keys_pressed[pygame.K_RIGHT]:
                if v.focus is not None:
                    v.focus += 1
                elif v.subpage in v.focus_order:
                    v.focus = 0
            v.on_focus_move = True
        if v.subpage in v.focus_order and v.focus is not None:
            if v.focus < 0:
                v.focus = len(v.focus_order[v.subpage])-1
            elif v.focus > len(v.focus_order[v.subpage])-1:
                v.focus = 0

    # -------------------------------------------------------------------------------------------- #

    def debug_messages() -> None:
        # Focus debug
        # if v.subpage in v.focus_order:
        #     if v.focus is not None:
        #         GraphUI.TextBox(f'[DEBUG] Focus {v.focus+1}/{len(v.focus_order[v.subpage])}',
        #                         v.W/2, 100, size=30, color=c.WHITE)
        #     else:
        #         GraphUI.TextBox('[DEBUG] Focus not initialized', v.W/2, 100, size=30, color=c.WHITE)
        # else:
        #     GraphUI.TextBox('[DEBUG] No focus here', v.W/2, 100, size=30, color=c.WHITE)
        # GraphUI.TextBox(v.game_chrono, 100, v.H/2, size=30, color=c.GUNMETAL)
        pass

    # -------------------------------------------------------------------------------------------- #

    def egg_control(n: int) -> None:
        if (pygame.time.get_ticks()-v.egg_start[n])/1000 >= 0.25:  # at least 0.25 sec between 2
            v.egg[n] = not v.egg[n]
            v.egg_start[n] = pygame.time.get_ticks()

    # -------------------------------------------------------------------------------------------- #

    def egg() -> None:
        if v.egg[0]:
            GraphUI.ImageBox('egg0', v.W/2, v.H/2)

    # -------------------------------------------------------------------------------------------- #

    def set_sounds() -> None:
        v.Sounds['click'] = pygame.mixer.Sound(v.SoundsPath['click'])
        v.Sounds['hover'] = pygame.mixer.Sound(v.SoundsPath['hover'])
        v.Sounds['bonus'] = pygame.mixer.Sound(v.SoundsPath['bonus'])
        v.Sounds['smash'] = pygame.mixer.Sound(v.SoundsPath['smash'])
        v.Sounds['kill'] = pygame.mixer.Sound(v.SoundsPath['kill'])
        pygame.mixer.Sound.set_volume(v.Sounds['click'], v.sound_volume)
        pygame.mixer.Sound.set_volume(v.Sounds['hover'], v.sound_volume)
        pygame.mixer.Sound.set_volume(v.Sounds['bonus'], v.sound_volume)
        pygame.mixer.Sound.set_volume(v.Sounds['smash'], v.sound_volume)
        pygame.mixer.Sound.set_volume(v.Sounds['kill'], v.sound_volume)

    # -------------------------------------------------------------------------------------------- #

    def start_music(path: str) -> None:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(v.music_volume)
        pygame.mixer.music.play(loops=-1, fade_ms=1000)

    # -------------------------------------------------------------------------------------------- #

    def stop_music() -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    # -------------------------------------------------------------------------------------------- #

    def format_time(ms: int) -> str:
        return '{:02d}:{:02d}'.format(int(ms/1000/60), int((ms/1000) % 60))

# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
