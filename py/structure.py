""" Projet Transverse - Groupe A3 - Fichier structure.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Python libraries
import pygame
import random
import datetime

# Internal modules
import variables as v
import constants as c
from ui import GraphUI
from ux import GameUX
from player import Player
import enemies as Enemies
import bonus as Bonus
import cursor
import controllers


# ___________________________________________ CLASSES ____________________________________________ #


class Struct:

    """ Class allowing to display the different pages of the game """

    # -------------------------------------------------------------------------------------------- #

    def unknown_page() -> None:
        GraphUI.TextBox('Unknown page', v.W/2, v.H/2)
        GraphUI.TextBox(f'Page : {v.page}/{v.subpage}', v.W/2, v.H/2+50, color=c.SILVER, size=20)

    # -------------------------------------------------------------------------------------------- #

    def loading_loop() -> None:
        i = 0
        loaded = False
        images_to_load = list(v.images_to_load.items())
        n = len(images_to_load)
        while v.running and not loaded:
            v.MousePos.click_down = c.DEF_POS
            v.MousePos.click_up = c.DEF_POS
            GameUX.handle_events()
            if i:
                v.mouse.update_position()
            v.screen.fill(c.DARK_SLATE_GRAY)

            GraphUI.TextBox(f'{round((i+1)/n*100)} %', v.W/2, v.H/2-100, size=60, color=c.GUNMETAL)
            GraphUI.TextBox('Please wait for loading', v.W/2, v.H/2-50, size=30, color=c.GUNMETAL)
            GraphUI.TextBox(images_to_load[i][1][0], v.W/2, v.H/2+50, size=20, color=c.SILVER)
            GraphUI.draw_rect(v.W/2, v.H/2, 400, 20, color=c.LAVENDER_BLUSH)
            GraphUI.draw_rect(v.W/2-200, v.H/2, ((i+1)/n)*400, 20, 'CL', color=c.BRIGHT_PINK)

            h = images_to_load[i]
            if h[0].startswith('player') or h[0].startswith('char'):
                for color in v.colors.keys():
                    v.Images[color+h[0]] = GraphUI.load_img(v.images_dir + h[1][0], color, *h[1][1])
            else:
                v.Images[h[0]] = GraphUI.load_img(v.images_dir+h[1][0], "", *h[1][1])
            i += 1
            if i == 1:
                v.mouse = cursor.Mouse()
            if i == n:
                loaded = True
            if i:
                GraphUI.ImageBox('cursor', v.mouse.rect.x, v.mouse.rect.y, 'TL')
            GameUX.egg()
            # v.clock.tick(v.FPS)
            pygame.display.update()

    # -------------------------------------------------------------------------------------------- #

    def home() -> None:
        v.bg_gif_idc += (v.tours % (v.FPS/c.BG_GIF_FPS) == 0)
        GraphUI.ImageBox(f'gif_menu_frame_{v.bg_gif_idc%c.NB_IMG_BG_GIF}', 0, 0, 'TL')

        GraphUI.ImageBox('title', v.W/2, v.H*2/5)
        GraphUI.wood_button('Play', v.W*1/4, v.H*3/4, event_id='play')
        GraphUI.wood_button('Options', v.W*2/4, v.H*3/4, event_id='options')
        GraphUI.wood_button('Quit', v.W*3/4, v.H*3/4, event_id='quit')
        GraphUI.ImageBox('cup', v.W-70, 70, event_id='leaderboard', hover_img=True)

        if v.focus_enter:
            v.Events['play'][1] = True

        if v.Events['play'][1]:
            v.focus = None
            v.nb_player = 0
            for i in range(4):
                v.Active[f'nb{i+1}'] = False
            v.Events['next'] = c.DEF_FALSE
            v.subpage = 'menu_arcade_choice_nb_players'
        elif v.Events['options'][1]:
            v.focus = None
            v.subpage = 'options'
        elif v.Events['quit'][1]:
            v.focus = None
            v.confirm_quit = True
        elif v.Events['leaderboard'][1]:
            v.focus = None
            v.to_sort = True
            v.subpage = 'leaderboard'
        if v.escape:
            v.focus = None
            v.confirm_quit = True

    # -------------------------------------------------------------------------------------------- #

    def break_() -> None:
        for player in v.Players_Group:
            player.tick = 0
        GraphUI.TextBox('Break', v.W/2, v.H/3, size=120)
        GraphUI.wood_button('Resume', v.W/4, v.H*4/5, event_id='resume')
        GraphUI.wood_button('Options', v.W*2/4, v.H*4/5, event_id='options')
        GraphUI.wood_button('Main menu', v.W*3/4, v.H*4/5, event_id='main_menu')

        if v.Events['resume'][1] or v.escape:
            v.focus = None
            v.subpage = 'game_arcade'
            v.countdown = True
            v.countdown_time = pygame.time.get_ticks()
            v.countdown_state = 3
            v.countdown_from_break = True
            v.start_game_session = pygame.time.get_ticks()
        elif v.Events['options'][1]:
            v.focus = None
            v.options_from_break = True
            v.page = 'menu'
            v.subpage = 'options'
        elif v.Events['main_menu'][1]:
            v.focus = None
            v.confirm_back_to_menu = True

    # -------------------------------------------------------------------------------------------- #

    def break_controller() -> None:
        for player in v.Players_Group:
            player.tick = 0
        GraphUI.TextBox('Controller disconnected', v.W/2, v.H/6, size=120, color=c.WHITE)
        GraphUI.TextBox('Please reconnecte controller or return to main menu',
                        v.W/2, v.H/2, size=60, color=c.SILVER)
        if controllers.disconnected_controller():
            GraphUI.wood_button('Main menu', v.W/2, v.H*4/5, event_id='main_menu')
        else:
            GraphUI.wood_button('Main menu', v.W*2/3, v.H*4/5, event_id='main_menu')
            GraphUI.wood_button('Resume', v.W/3, v.H*4/5, event_id='resume')
            if v.focus_enter:
                v.Events['Resume'][1] = True

        if v.Events['resume'][1]:
            v.focus = None
            v.subpage = 'game_arcade'
            v.Events['resume'][1] = False
            controllers.connect_controllers()
            v.countdown = True
            v.countdown_time = pygame.time.get_ticks()
            v.countdown_state = 3
            v.countdown_from_break = True
            v.start_game_session = pygame.time.get_ticks()
        elif v.Events['main_menu'][1]:
            v.focus = None
            v.confirm_back_to_menu = True

    # -------------------------------------------------------------------------------------------- #

    def endgame() -> None:
        GraphUI.TextBox('End game', v.W/2, v.H/3, size=120)
        GraphUI.wood_button('Main menu', v.W/4, v.H*4/5, event_id='main_menu')
        GraphUI.wood_button('Play Again', v.W*3/4, v.H*4/5, event_id='next')
        GraphUI.wood_button('Quit', v.W*2/4, v.H*4/5, event_id='quit')

        if v.focus_enter:
            v.Events['Main menu'][1] = True

        if v.Events['main_menu'][1]:
            v.focus = None
            v.page = 'menu'
            v.subpage = 'home'
            GameUX.stop_music()
            GameUX.start_music(v.MusicPaths['menu_music'])
        elif v.Events['quit'][1]:
            v.confirm_quit = True

    # -------------------------------------------------------------------------------------------- #

    def load_arcade() -> None:
        GameUX.stop_music()
        GameUX.start_music(v.MusicPaths['game_music'])

        v.Players_Group = pygame.sprite.Group()
        v.Enemies_Group = pygame.sprite.Group()
        v.Bonus_Group = pygame.sprite.Group()

        """
        for i in range(r.randint(3, 7)):
                v.Enemies_Group.add(r.choice([
                    Enemies.Boar(v.Players_Group.sprites()[0], 400 + r.randint(1, 5) * 75),
                    Enemies.Goblin(v.Players_Group.sprites()[0], 400 + r.randint(1, 5) * 75),
                    Enemies.Eye(v.Players_Group.sprites()[0], 400 + r.randint(1, 5) * 75)]))
        """
        map_grid = v.Maps[f'{v.map_choice}'.capitalize()]
        for y in range(len(map_grid)):
            for x in range(len(map_grid[y])):
                if map_grid[y][x] == -1 and len(v.Players_Group) < v.nb_player:
                    q = c.TILE_SIZE
                    v.Players_Group.add(Player((x * q + q//2, y * q + q), len(v.Players_Group)))

        for i in range(pygame.joystick.get_count()):
            if v.Players_Group.sprites()[i].controller is None:
                v.Players_Group.sprites()[i].controller = pygame.joystick.Joystick(i)

        v.level.update_actual_map()
        v.countdown = True
        v.countdown_time = pygame.time.get_ticks()
        v.countdown_state = 3
        v.game_chrono = 0
        v.start_game_session = pygame.time.get_ticks()
        v.stop_game_session = 0
        v.subpage = 'game_arcade'

    # -------------------------------------------------------------------------------------------- #

    def game_arcade() -> None:
        v.camera.display()
        map_grid = v.Maps[f'{v.map_choice}'.capitalize()]
        if v.countdown:
            GraphUI.TextBox(v.countdown_state if v.countdown_state else 'FIGHT !', v.W/2, v.H/3,
                            color=c.WHITE, size=200)
            if v.countdown_state >= 0 and (pygame.time.get_ticks()-v.countdown_time)/1000 >= 1:
                v.countdown_time = pygame.time.get_ticks()
                v.countdown_state -= 1
            if v.countdown_state < (0 if not v.countdown_from_break else 1):
                v.countdown = False
                v.countdown_from_break = False
        else:
            if not controllers.disconnected_controller():
                nb_dead_players = 0
                for player in v.Players_Group.sprites():
                    if player.state == 'death' and player.frame >= 11:
                        nb_dead_players += 1
                if nb_dead_players == v.nb_player:
                    v.subpage = 'endgame' 
                else:  
                    for y in range(len(map_grid)):
                        for x in range(len(map_grid[y])):
                            if map_grid[y][x] == -2 and not random.randint(0, 150 - 1) and len(v.Enemies_Group) < 10:
                                rand = random.randint(1, 3)
                                if rand == 1:
                                    v.Enemies_Group.add(Enemies.Boar((x * c.TILE_SIZE + c.TILE_SIZE//2, y * c.TILE_SIZE + c.TILE_SIZE)))
                                elif rand == 2:
                                    v.Enemies_Group.add(Enemies.Goblin((x * c.TILE_SIZE + c.TILE_SIZE//2, y * c.TILE_SIZE + c.TILE_SIZE)))
                                elif rand == 3:
                                    v.Enemies_Group.add(Enemies.BringerofDeath((x * c.TILE_SIZE + c.TILE_SIZE//2, y * c.TILE_SIZE + c.TILE_SIZE))) 
                            
                            elif map_grid[y][x] == -3 and not random.randint(0, v.random_bonus_spawn) and v.nb_bonus < v.nb_player * 2 \
                                    and any(bonus.rect for bonus in v.Bonus_Group) != (x * c.TILE_SIZE + c.TILE_SIZE//2, y * c.TILE_SIZE + c.TILE_SIZE):
                                potion_choice = random.randint(1, 3)
                                if potion_choice == 1:
                                    if v.potion_coordinates['life_potion'] == [-1, -1]:
                                        v.Bonus_Group.add(Bonus.LifePotion((x * c.TILE_SIZE + c.TILE_SIZE//2, y * c.TILE_SIZE + c.TILE_SIZE)))
                                        v.potion_coordinates['life_potion'] = y, x
                                elif potion_choice == 2:
                                    if v.potion_coordinates['speed_potion'] == [-1, -1]:
                                        v.Bonus_Group.add(Bonus.SpeedPotion((x * c.TILE_SIZE + c.TILE_SIZE//2, y * c.TILE_SIZE + c.TILE_SIZE)))
                                        v.potion_coordinates['speed_potion'] = y, x
                                elif potion_choice == 3:
                                    if v.potion_coordinates['power_potion'] == [-1, -1]:
                                        v.Bonus_Group.add(Bonus.PowerPotion((x * c.TILE_SIZE + c.TILE_SIZE//2, y * c.TILE_SIZE + c.TILE_SIZE)))
                                        v.potion_coordinates['power_potion'] = y, x
                                v.nb_bonus += 1

                    for player in v.Players_Group:
                        if player.tick == 0:
                            player.tick = pygame.time.get_ticks()
                        controllers.get_inputs_players(player)
                        v.level.movement_collisions(player)
                        if player.lives <= 0 and player.state != 'death':
                            player.state = 'death'
                            player.frame = 1

                    for enemy in v.Enemies_Group:
                        if enemy.tick == 0:
                            enemy.tick = pygame.time.get_ticks()
                        enemy.update()
                        v.level.movement_collisions(enemy)
                        if enemy.lives <= 0 and enemy.state != 'death':
                            pygame.mixer.Sound.play(v.Music['kill'])
                            enemy.state = 'death'
                            enemy.frame = 1
                            enemy.death_timer = pygame.time.get_ticks()
                            v.nb_enemies -= 1

                    for bonus in v.Bonus_Group:
                        if not bonus.active:
                            
                            if bonus.name == 'life_potion':
                                v.potion_coordinates['life_potion'] = [-1, -1]
                            elif bonus.name == 'speed_potion':
                                v.potion_coordinates['speed_potion'] = [-1, -1]
                            elif bonus.name == 'power_potion':
                                v.potion_coordinates['power_potion'] = [-1, -1]

                            v.Bonus_Group.remove(bonus)
                            v.nb_bonus -= 1

                
            else:
                v.subpage = 'break_controller'
                v.start_game_session = 0
                v.stop_game_session = v.game_chrono
            GraphUI.TextBox(GameUX.format_time(v.game_chrono), v.W/2, 50,
                            color=v.maps_text_color[v.map_choice], size=45)
            v.game_chrono = pygame.time.get_ticks() - v.start_game_session + v.stop_game_session
            if v.game_chrono >= 60 * 10 ** 3 and v.verif_random == 0:
                v.random_enemies_spawn -= 50
                v.random_bonus_spawn += 150
                v.verif_random = 1
            elif v.game_chrono >= 5 * 60 * 10 ** 3 and v.verif_random == 1:
                v.random_enemies_spawn -= 50
                v.random_bonus_spawn += 150
                v.verif_random = 2
            elif v.game_chrono >= 10 * 60 * 10 ** 3 and v.verif_random == 2:
                v.random_enemies_spawn -= 100
                v.random_bonus_spawn += 200
                v.verif_random = 3
        if v.show_fps:
            GraphUI.TextBox(round(v.clock.get_fps()), v.W-20, 15, 'TR',
                            color=v.maps_text_color[v.map_choice], size=20)
        if v.escape:
            v.subpage = 'break_'
            v.start_game_session = 0
            v.stop_game_session = v.game_chrono
            v.countdown = False

    # -------------------------------------------------------------------------------------------- #

    def menu_arcade_options() -> None:
        GraphUI.ImageBox('left_arrow', 50, 50, event_id='return', hover_img=True)

        GraphUI.TextBox('Game settings', v.W/2, v.H*4/25, color=c.GUNMETAL, size=60)

        GraphUI.TextBox('Hardcore mode', v.W*1/3, v.H*8/25, color=c.WHITE)
        v.hardcore = GraphUI.on_off_button(v.W*2/3, v.H*8/25, 'hardcore')

        x = GraphUI.TextBox('Show FPS', v.W*1/3, v.H*12/25, color=c.WHITE)
        v.show_fps = GraphUI.on_off_button(v.W*2/3, v.H*12/25, 'fps_onoff')

        GraphUI.TextBox('(Press F11 to switch in game)', x.L+x.W/2, x.T+x.H+20,
                        color=c.SILVER, size=20)

        if not v.hardcore:
            GraphUI.TextBox('Number of lives', v.W*1/3, v.H*16/25, color=c.WHITE)
            v.nb_lives = GraphUI.value_slider(v.W*2/3, v.H*16/25, 420, 60,
                                              'slider_lives', c.SLIDER_UNDER)
        else:
            GraphUI.TextBox('Number of lives', v.W*1/3, v.H*16/25, color=c.DIM_GRAY)
            v.nb_lives = GraphUI.value_slider(v.W*2/3, v.H*16/25, 420, 60,
                                              'slider_lives', c.SLIDER_UNDER,
                                              disable=True, freezevalue=1)
            v.nb_lives = 1

        if v.show_fps:
            GraphUI.TextBox(round(v.clock.get_fps()), v.W-20, 15, 'TR',
                            color=c.BLACK, size=20)

        GraphUI.wood_button('VALIDATE', v.W/2, v.H*4/5, event_id='next')

        if v.focus_enter:
            v.Events['next'][1] = True

        if v.Events['return'][1] or v.escape:
            v.focus = None
            v.subpage = 'menu_arcade_choice_map'
        elif v.Events['next'][1]:
            v.focus = None
            v.page = 'game'
            v.subpage = 'load_arcade'

    # -------------------------------------------------------------------------------------------- #

    def options() -> None:
        GraphUI.ImageBox('left_arrow', 50, 50, event_id='return', hover_img=True)

        GraphUI.TextBox('Max FPS', v.W*1/3, v.H*1/4, color=c.WHITE)
        v.FPS = GraphUI.value_slider(v.W*2/3, v.H*1/4, 420, 60, 'fps', c.SLIDER_UNDER, 'FPS')

        GraphUI.TextBox('Sounds', v.W*1/3, v.H*2/4, color=c.WHITE)
        s2 = GraphUI.slider(v.W*2/3, v.H*2/4, 420, 60, slider_id='slider_sound',
                            button_color=c.SLIDER_BUTTON, over_color=c.SLIDER_OVER,
                            under_color=c.SLIDER_UNDER, unit='%')

        GraphUI.TextBox('Music', v.W*1/3, v.H*3/4, color=c.WHITE)
        s3 = GraphUI.slider(v.W*2/3, v.H*3/4, 420, 60, slider_id='slider_music',
                            button_color=c.SLIDER_BUTTON, over_color=c.SLIDER_OVER,
                            under_color=c.SLIDER_UNDER, unit='%')

        if v.sound_volume != s2/100:
            v.sound_volume = s2/100
            for i in v.Sounds:
                pygame.mixer.Sound.set_volume(v.Sounds[i], v.sound_volume)
        if v.music_volume != s3/100:
            v.music_volume = s3/100
            pygame.mixer.music.set_volume(v.music_volume)

        if v.Events['return'][1] or v.escape:
            v.focus = None
            if v.options_from_game:
                v.page = 'game'
                v.subpage = 'game_arcade'
                v.options_from_game = False
            elif v.options_from_break:
                v.page = 'game'
                v.subpage = 'break_'
                v.options_from_break = False
            else:
                v.subpage = 'home'

    # -------------------------------------------------------------------------------------------- #

    def confirm_quit() -> None:
        v.Events['quit'][0] = False
        GraphUI.draw_rect(0, 0, v.W, v.H, 'TL', color=c.WHITE, alpha=0.7)
        GraphUI.draw_rect(v.W/2, v.H/2, v.W/2, v.H/2, color=c.LIGHT_SLATE_GRAY, border_radius=60)
        GraphUI.TextBox('Do you want to quit ?', v.W/2, v.H*3/8, color=c.GUNMETAL)
        GraphUI.TextBox('', v.W/2, v.H*3/8+75, color=c.GUNMETAL, size=25)
        GraphUI.wood_button('Yes', v.W*3/8, v.H*5/8, event_id='yes_quit', except_button=True)
        GraphUI.wood_button('No', v.W*5/8, v.H*5/8, event_id='no_stay', except_button=True)

        if v.focus_enter:
            v.Events['yes_quit'][1] = True

        if v.Events['yes_quit'][1]:
            v.focus = None
            v.running = False
            v.wait_for_next_click = True
        elif v.Events['no_stay'][1]:
            v.focus = None
            v.confirm_quit = False

            v.wait_for_next_click = True

    # -------------------------------------------------------------------------------------------- #

    def confirm_back_to_menu() -> None:
        v.Events['main_menu'][0] = False
        GraphUI.draw_rect(0, 0, v.W, v.H, 'TL', color=c.WHITE, alpha=0.7)
        GraphUI.draw_rect(v.W/2, v.H/2, v.W/2, v.H/2, color=c.LIGHT_SLATE_GRAY, border_radius=60)
        GraphUI.TextBox('Do you want to return to the menu ?', v.W/2, v.H*3/8, color=c.GUNMETAL)
        GraphUI.TextBox('Progress will be lost', v.W/2, v.H*3/8+75, color=c.GUNMETAL, size=25)
        GraphUI.wood_button('Yes', v.W*3/8, v.H*5/8, event_id='btm_yes', except_button=True)
        GraphUI.wood_button('No', v.W*5/8, v.H*5/8, event_id='btm_no', except_button=True)

        if v.Events['btm_yes'][1]:
            v.focus = None
            v.page = 'menu'
            v.subpage = 'home'
            v.confirm_back_to_menu = False
            GameUX.stop_music()
            GameUX.start_music(v.MusicPaths['menu_music'])
            v.wait_for_next_click = True
        if v.Events['btm_no'][1]:
            v.focus = None
            v.confirm_back_to_menu = False
            v.escape = False
            v.wait_for_next_click = True

    # -------------------------------------------------------------------------------------------- #

    def menu_arcade_choice_nb_players() -> None:
        GraphUI.ImageBox('left_arrow', 50, 50, event_id='return', hover_img=True)
        if not v.nb_player:
            if len(v.focus_order['menu_arcade_choice_nb_players']) > 5:
                v.focus_order['menu_arcade_choice_nb_players'].pop()
            GraphUI.TextBox('Choose the number of players', v.W/2, v.H*4/5, color=c.WHITE)
        else:
            if len(v.focus_order['menu_arcade_choice_nb_players']) < 6:
                v.focus_order['menu_arcade_choice_nb_players'].append('next')
            GraphUI.wood_button('VALIDATE', v.W/2, v.H*4/5, event_id='next')
            if v.focus_enter:
                v.Events['next'][1] = True

        for i in range(2):
            for j in range(2):
                k = 2*i+j
                f = f'nb{k+1}'
                GraphUI.text_button(k+1, v.W*(j+1)/3, v.H*(i+1)/4, 300, 180, event_id=f)
                if v.Events[f][1]:
                    v.Active[f] = not v.Active[f]
                    if v.nb_player:
                        v.Active[f'nb{v.nb_player}'] = False
                    v.nb_player = k+1 if v.Active[f] else 0
        v.nb_enemies = 1.5**(v.nb_player-1)
        if v.Events['return'][1] or v.escape:
            v.focus = None
            v.subpage = 'home'
        elif v.nb_player and v.Events['next'][1]:
            v.focus = None
            v.id_players = [-2, -2, -2, -2]
            v.nb_char_chosen = 0
            v.all_chosen = False
            v.player_choices = {f'P{i+1}': None for i in range(4)}
            for i in range(4):
                v.Active[f'char{i+1}'] = False
            v.subpage = 'menu_arcade_choice_characters'

    # -------------------------------------------------------------------------------------------- #

    def menu_arcade_controllers() -> None:
        v.Events['next'][1] = 0
        if v.nb_player - 1 > pygame.joystick.get_count():
            GraphUI.TextBox('Not enough controller', v.W/2, v.H*4/5, color=c.WHITE)
        elif v.nb_player < pygame.joystick.get_count():
            GraphUI.TextBox('Too many controllers', v.W/2, v.H*4/5, color=c.WHITE)
        elif v.nb_player == pygame.joystick.get_count():
            for i in range(v.nb_player):
                v.id_players[i] = i
        else:
            v.id_players[0] = -1
            for i in range(1, v.nb_player):
                v.id_players[i] = i - 1
        v.nb_controllers = pygame.joystick.get_count()
        if v.id_players[0] != -2:
            GraphUI.wood_button('VALIDATE', v.W/2, v.H*4/5, event_id='next')
            if v.focus_enter:
                v.Events['next'][1] = True
        GraphUI.ImageBox('left_arrow', 50, 50, event_id='return', hover_img=True)
        GraphUI.TextBox('Menu arcade controllers', v.W/2, v.H*1/6, color=c.WHITE)
        v.controllers = []
        for i in range(v.nb_controllers):
            v.controllers.append(pygame.joystick.Joystick(i))
        for i in range(v.nb_player):
            GraphUI.TextBox(v.player_names[f'P{i+1}'], v.W*1/3, v.H*(i+3)/10, color=v.colors[v.associated_names[v.player_choices[f'P{i+1}']]])
            if v.id_players[i] != -2:
                controllers.menu_controllers(i)
            if v.actions_players[i] != []:
                GraphUI.TextBox('Valid', v.W*3/4, v.H*(i+3)/10, color=c.GREEN)
        if v.Events['return'][1] or v.escape:
            v.focus = None
            v.subpage = 'menu_arcade_choice_names'
        elif v.Events['next'][1]:
            v.focus = None
            v.subpage = 'menu_arcade_choice_map'

    # -------------------------------------------------------------------------------------------- #

    def menu_arcade_choice_characters() -> None:
        GraphUI.ImageBox('left_arrow', 50, 50, event_id='return', hover_img=True)
        char_ids = list(v.associated_names)
        char_names = list(v.associated_names.values())
        player_color = [c.COLOR_P1, c.COLOR_P2, c.COLOR_P3, c.COLOR_P4]
        for i in range(2):
            for j in range(2):
                k = 2*i+j  # char indice
                x, y = v.W*(j+1)/3, v.H*(i+1)/4
                GraphUI.draw_rect(x, y+10, 300, 180, border_radius=20, color=c.DARK_SLATE_GRAY,
                                  event_id=char_ids[k])
                if (v.Events[char_ids[k]][0] and not v.all_chosen) or v.Active[char_ids[k]]:
                    GraphUI.draw_rect(x, y+10, 300, 180, color=c.CAMBRIDGE_BLUE, border_radius=20)
                if v.Active[char_ids[k]]:
                    GraphUI.draw_rect(x, y+10, 300, 180, border_radius=20, border_width=3,
                                      color=player_color[k])
                z = GraphUI.ImageBox(f'{list(v.colors.keys())[k]}player_idle_1', x, y)
                corresp_player = None
                for w in v.player_choices:
                    if v.player_choices[w] == f'char{k+1}':
                        corresp_player = w
                        break
                player_txt = f' - {corresp_player}' if corresp_player is not None else ''
                GraphUI.TextBox(char_names[k]+player_txt, z.L+z.W/2, z.T+z.H+30, color=c.SILVER,
                                size=25)
                if v.Events[char_ids[k]][1] and (not v.all_chosen or v.Active[char_ids[k]]):
                    if not v.Active[char_ids[k]]:
                        v.Active[char_ids[k]] = True
                        v.nb_char_chosen += 1
                        v.player_choices[f'P{v.nb_char_chosen}'] = f'char{k+1}'
                    else:
                        start_p = int(corresp_player[1:])
                        for h in range(start_p, 5):
                            v.Active[v.player_choices[f'P{h}']] = False
                            v.player_choices[f'P{h}'] = None
                        v.nb_char_chosen = start_p-1
        v.all_chosen = v.nb_char_chosen == v.nb_player
        if not v.nb_player:
            GraphUI.TextBox('There are no players', v.W/2, v.H*4/5, color=c.WHITE)
        elif not v.all_chosen:
            GraphUI.TextBox(f'Choose P{v.nb_char_chosen+1} character', v.W/2, v.H*4/5,
                            color=c.WHITE)
        else:
            GraphUI.wood_button('VALIDATE', v.W/2, v.H*4/5, event_id='next')
            if v.focus_enter:
                v.Events['next'][1] = True
        if v.Events['return'][1] or v.escape:
            v.focus = None
            v.subpage = 'menu_arcade_choice_nb_players'
        elif v.nb_player and v.all_chosen and v.Events['next'][1]:
            v.Events['next'][1] = False
            v.focus = None
            v.map_choice = None
            for i in range(3):
                v.Active[f'map{i+1}'] = False
            v.subpage = 'menu_arcade_choice_names'
            v.field_focus = None

    # -------------------------------------------------------------------------------------------- #

    def menu_arcade_choice_names() -> None:
        v.nb_fields = v.nb_player
        GraphUI.ImageBox('left_arrow', 50, 50, event_id='return', hover_img=True)

        for i, p in enumerate(v.player_choices):
            if v.player_choices[p] is not None:
                x = f'name{i+1}'
                color_ = v.colors[v.associated_names[v.player_choices[p]]]
                GraphUI.TextBox(f'Player{i+1}', v.W/3, v.H*(i+3)/10, color=color_, size=35)
                v.player_names[p] = GraphUI.TextInput(v.W*2/3, v.H*(i+3)/10, 420, 60,
                                                      field_id=x, value=v.player_names[p])
                GraphUI.ImageBox('random', v.W*2/3+420/2+50, v.H*(i+3)/10,
                                 event_id=f'random_name{i+1}', hover_img=True)
                if v.Events[f'random_name{i+1}'][0]:
                    GraphUI.TextBox('Random', v.W*2/3+420/2+50, v.H*(i+3)/10+50,
                                    color=c.SILVER, size=20)
                if v.Events[f'random_name{i+1}'][1]:
                    v.player_names[p] = random.choice(v.RandomNames)
                if v.Events[x][1]:
                    if v.Active[x]:
                        v.Active[x] = False
                        v.field_focus = None
                    else:
                        for j in range(v.nb_fields):
                            v.Active[f'name{j+1}'] = (i == j)
                        v.field_focus = i
                    v.text_input = False
                    v.text_overflow = False

                if v.Active[x] and v.field_enter:
                    v.field_enter = False
                    v.Active[x] = False
                    v.text_input = False
                    v.text_overflow = False
                    if v.field_focus < v.nb_fields-1:
                        v.field_focus += 1
                        v.Active[f'name{v.field_focus+1}'] = True
                    else:
                        v.field_focus = v.nb_fields

        if all(v.player_names[i] for i in v.player_names if v.player_choices[i] is not None):
            GraphUI.wood_button('VALIDATE', v.W/2, v.H*4/5, event_id='next')
            if v.field_enter and (v.field_focus is None or v.field_focus == v.nb_fields):
                v.Events['next'][1] = True
        else:
            GraphUI.TextBox('Enter player usernames to continue', v.W/2, v.H*4/5, color=c.WHITE)
        if v.Events['return'][1] or v.escape:
            v.focus = None
            v.subpage = 'menu_arcade_choice_characters'
        elif v.Events['next'][1]:
            v.focus = None
            v.subpage = 'menu_arcade_controllers'

    # -------------------------------------------------------------------------------------------- #

    def menu_arcade_choice_map() -> None:
        GraphUI.ImageBox('left_arrow', 50, 50, event_id='return', hover_img=True)
        bg_names = ['Forest map', 'Mountain map', 'Sky map']
        for i in range(3):
            k = f'map{i+1}'
            GraphUI.ImageBox(k+'_bg1_lil', v.W*(i+1)/4, v.H*3/7)
            GraphUI.ImageBox(k+'_bg2_lil', v.W*(i+1)/4, v.H*3/7)
            z = GraphUI.ImageBox(k+'_bg3_lil', v.W*(i+1)/4, v.H*3/7, event_id=k)
            GraphUI.TextBox(bg_names[i], z.L+z.W/2, z.T+z.H+30, color=c.SILVER, size=25)
            if v.Events[k][0]:
                GraphUI.draw_border(z.L, z.T, z.W, z.H, border_width=3, border_color=c.ASH_GRAY)
            if v.map_choice == k:
                GraphUI.draw_border(z.L, z.T, z.W, z.H, border_width=3,
                                    border_color=c.AMARANTH_PURPLE)
            if v.Events[k][1]:
                v.Active[k] = not v.Active[k]
                if v.map_choice is not None:
                    v.Active[v.map_choice] = False
                v.map_choice = k if v.Active[k] else None
        if v.map_choice is None:
            GraphUI.TextBox('Choose the map', v.W/2, v.H*4/5, color=c.WHITE)
        else:
            GraphUI.wood_button('VALIDATE', v.W/2, v.H*4/5, event_id='next')
            if v.focus_enter:
                v.Events['next'][1] = True
        if v.Events['return'][1] or v.escape:
            v.focus = None
            v.subpage = 'menu_arcade_controllers'
        elif v.map_choice is not None and v.Events['next'][1]:
            v.focus = None
            v.subpage = 'menu_arcade_options'

    # -------------------------------------------------------------------------------------------- #

    class KeyFunctions:

        def sort_function(item: str) -> float or str:
            if v.filter_[0] == 'sort_score':
                return Struct.KeyFunctions.sort_by_score(item)
            elif v.filter_[0] == 'sort_player':
                return Struct.KeyFunctions.sort_by_player(item)
            elif v.filter_[0] == 'sort_date':
                return Struct.KeyFunctions.sort_by_date(item)

        def sort_by_score(item: str) -> float:
            minutes, seconds = item['score'].replace(' min ', '.').replace(' s', '').split('.')
            return float(minutes)*60 + float(seconds)

        def sort_by_player(item: str) -> str:
            return item['name']

        def sort_by_date(item: str) -> float:
            return datetime.datetime.strptime(item['date'], '%d/%m/%Y %H:%M')

    # -------------------------------------------------------------------------------------------- #

    def leaderboard() -> None:
        if v.to_sort:
            v.LeaderboardSorted = sorted(v.Leaderboard['list'],
                                         key=Struct.KeyFunctions.sort_function,
                                         reverse=(v.filter_[1] == 'desc'))
            v.Top3 = sorted(v.Leaderboard['list'], key=Struct.KeyFunctions.sort_by_score,
                            reverse=True)[:3]
            v.Top3_names = [i['name'] for i in v.Top3]
            v.to_sort = False
        a = 'sort_asc' if v.Filters['sort_score'] == 'desc' else 'sort_desc'
        b = 'sort_asc' if v.Filters['sort_player'] == 'desc' else 'sort_desc'
        d = 'sort_asc' if v.Filters['sort_date'] == 'desc' else 'sort_desc'
        GraphUI.ImageBox('left_arrow', 50, 50, event_id='return', hover_img=True)
        if v.focus_enter:
            v.Events['return'][1] = True
        GraphUI.TextBox('Leaderboard', v.W/2, v.H*2/16, color=c.WHITE, size=70)
        x = GraphUI.TextBox('Time', v.W*1/4, v.H*4/16, size=35, color=c.WHITE)
        GraphUI.ImageBox(a, x.L+x.W+40, x.T+x.H/2, event_id='sort_score', hover_img=True)
        y = GraphUI.TextBox('Player', v.W*2/4, v.H*4/16, size=35, color=c.WHITE)
        GraphUI.ImageBox(b, y.L+y.W+40, y.T+y.H/2, event_id='sort_player', hover_img=True)
        z = GraphUI.TextBox('Date', v.W*3/4, v.H*4/16, size=35, color=c.WHITE)
        GraphUI.ImageBox(d, z.L+z.W+40, z.T+z.H/2, event_id='sort_date', hover_img=True)
        p = {1: None, 2: None, 3: None}
        for i, item in enumerate(v.LeaderboardSorted[:10]):
            GraphUI.TextBox(item['score'], v.W*1/4, v.H*(i+5.5)/16, size=30, color=c.SILVER)
            t = GraphUI.TextBox(item['name'], v.W*2/4, v.H*(i+5.5)/16, size=30, color=c.SILVER)
            GraphUI.TextBox(item['date'], v.W*3/4, v.H*(i+5.5)/16, size=30, color=c.SILVER)
            if item['name'] in v.Top3_names:
                p[v.Top3_names.index(item['name'])+1] = i
        if p[1] is not None:
            GraphUI.ImageBox('first', t.L-40, v.H*(p[1]+5.5)/16)
        if p[2] is not None:
            GraphUI.ImageBox('second', t.L-40, v.H*(p[2]+5.5)/16)
        if p[3] is not None:
            GraphUI.ImageBox('third', t.L-40, v.H*(p[3]+5.5)/16)
        for sort_mode in v.Filters:
            if v.Events[sort_mode][1]:
                v.to_sort = True
                v.filter_ = (sort_mode, v.Filters[sort_mode])
                v.Filters[sort_mode] = 'desc' if v.Filters[sort_mode] == 'asc' else 'asc'
        if v.Events['return'][1] or v.escape:
            v.focus = None
            v.subpage = 'home'

# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
