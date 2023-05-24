""" Projet Transverse - Groupe A3 - Fichier ui.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Python libraries
import pygame

# Internal modules
import variables as v
import constants as c


# ___________________________________________ CLASSES ____________________________________________ #


class GraphUI:

    """ Manages graphic display with Pygame """

    # -------------------------------------------------------------------------------------------- #

    def load_img(path: str, player_color: str, width: int = -1, height: int = -1) -> pygame.Surface:
        """ Allows to load an image (whose path is specified by :path:) and to resize it either
        strictly (:width:, :height:) or autoscale (by specifying only :width: or only :height:) or
        not to resize it (by not specifying :width: or :height:). """
        return GraphUI.resize_img(pygame.image.load(path), player_color, width, height)

    # -------------------------------------------------------------------------------------------- #

    def resize_img(img: pygame.Surface, player_color: str, width: int = -1, height: int = -1) -> pygame.Surface:
        """ Allows to resize an image either strictly (:width:, :height:) or autoscale
        (by specifying only :width: or only :height:) or not to resize it
        (by not specifying :width: or :height:). """
        img_width = img.get_width()
        img_height = img.get_height()
        if width >= 0 and height >= 0:
            img = pygame.transform.scale(img, (round(width), round(height)))
        elif width >= 0 and height < 0:
            img = pygame.transform.scale(img, (round(width), round(img_height * width / img_width)))
        elif width < 0 and height >= 0:
            img = pygame.transform.scale(img, (round(img_width * height / img_height),
                                               round(height)))

        if player_color != "":
            return GraphUI.color_players(img, player_color)
        else:
            return img.convert_alpha()

    # -------------------------------------------------------------------------------------------- #

    def color_players(img: pygame.Surface, player_color):
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                px = img.get_at((x, y))
                if px[3] != 0:  # alpha
                    if player_color == 'Red':
                        img.set_at((x, y), (px[0], px[1]//1.5, px[2]//1.5, px[3]))  # Set the color of the pixel.
                    elif player_color == 'Green':
                        img.set_at((x, y), (px[0]//1.3, px[1], px[2]//1.3, px[3]))
                    elif player_color == 'Blue':
                        img.set_at((x, y), (px[0], px[1], min(px[2]*1.5, 255), px[3]))
                    elif player_color == 'Purple':
                        img.set_at((x, y), (min(px[0]*1.5, 255), px[1], min(px[2]*1.5, 255), px[3]))
        return img.convert_alpha()

    # -------------------------------------------------------------------------------------------- #

    def handle_collide_events(obj: pygame.Rect, event_id: str, except_button: bool = False) -> None:
        if v.wait_for_next_click:
            v.MousePos.click_down = c.DEF_POS
            v.MousePos.click_up = c.DEF_POS
        if (not v.confirm_quit) or (not v.confirm_back_to_menu) or except_button:
            assert event_id in v.Events, f'event_id \'{event_id}\''
            events_copy = v.Events[event_id]
            v.Events[event_id] = [obj.collidepoint(v.MousePos.end_motion),
                                  obj.collidepoint(v.MousePos.click_up),
                                  obj.collidepoint(v.MousePos.click_down)]
            if v.Events[event_id][0] and not events_copy[0]:
                pygame.mixer.Sound.play(v.Sounds['hover'])
            if v.Events[event_id][1] and not events_copy[1]:
                pygame.mixer.Sound.play(v.Sounds['click'])

    # -------------------------------------------------------------------------------------------- #

    def hover_color(color: tuple, incr: int = 50, incr_alpha: int = 0.1) -> tuple:
        """ Returns a lightened (:incr: > 0) or darkened (:incr: < 0) color from an
        initial RGB :color:, respectively a lightened (:incr_alpha: > 0) or darkened
        (:incr_alpha: < 0) opacity for the alpha parameter in initial RGBA :color:.
        Note that 0 <= :incr_alpha: <= 1. """
        assert 3 <= len(color) <= 4, 'invalid color format'
        if len(color) == 4:
            if incr_alpha >= 0:
                color = pygame.Color(color) + pygame.Color(0, 0, 0, round(incr_alpha*255))
            else:
                color = pygame.Color(color) - pygame.Color(0, 0, 0, round(abs(incr_alpha)*255))
            if incr >= 0:
                color = pygame.Color(color) + pygame.Color(incr, incr, incr, 0)
            else:
                color = pygame.Color(color) - pygame.Color(abs(incr), abs(incr), abs(incr), 0)
        else:
            if incr >= 0:
                color = pygame.Color(color) + pygame.Color(incr, incr, incr)
            else:
                color = pygame.Color(color) - pygame.Color(abs(incr), abs(incr), abs(incr))
        return color

    # -------------------------------------------------------------------------------------------- #

    def color_leaning_to_black(color: tuple):
        """ Returns True if the :color: leans more towards black than towards white,
        False otherwise """
        return 0.2126*color[0] + 0.7152*color[1] + 0.0722*color[2] < 128

    # -------------------------------------------------------------------------------------------- #

    def get_LT_by_LT_code_pos(LT_code_pos: str, L: int, T: int, W: int, H: int) -> tuple:
        """ Returns the relative position (:L:, :T:) which moves the dimension (:L:, :T:, :W:, :H:)
         depending on the :LT_code_pos: specified (see 2nd "get_LT_by_LT_code_pos" docstring). """

        """
              TL          TC        TR
               X----------X----------X
               |                     |
               |          CC         |
            CL X          X          X CR
               |                     |
               |                     |
               X----------X----------X
              BL          BC        BR
        """
        assert LT_code_pos in ('TL', 'TC', 'TR', 'CL', 'CC', 'CR', 'BL', 'BC', 'BR'), \
            f'code invalid : {LT_code_pos}'
        L -= (LT_code_pos[1] == 'C') * W/2 + (LT_code_pos[1] == 'R') * W
        T -= (LT_code_pos[0] == 'C') * H/2 + (LT_code_pos[0] == 'B') * H
        return L, T

    # -------------------------------------------------------------------------------------------- #

    def center(L: int, T: int, W: int, H: int) -> tuple:
        """ Special case of the "get_LT_by_LT_code_pos" function, to center an element of
        dimensions (:L:, :T:, :W:, :H:) """
        return *GraphUI.get_LT_by_LT_code_pos('CC', L, T, W, H), W, H

    # -------------------------------------------------------------------------------------------- #

    class TextBox:
        """ Displays text :text: on the screen at position (:L:, :T:). If the arguments are
        specified, it is also possible to specify the relative position code :LT_code_pos:
        (see docstring "get_LT_by_LT_code_pos"), the :event_id:, the :size:, the :color:,
        the presence of a :border:, and if so the :border_color: and the :border_width:.
        Attributes : L, T, W, H, text_render, text_rect. """

        """ Using a class provides access to attributes after text box display. """

        def __init__(self, text: str, L: int, T: int, LT_code_pos: str = 'CC', event_id: str = '',
                     size: int = 50, color: tuple = c.GUNMETAL, font_id: str = v.default_font,
                     border: str = False, border_color: tuple = c.RED,
                     border_width: int = 1) -> None:
            font = pygame.font.Font(v.Fonts[font_id], size)
            self.text_render = font.render(str(text), True, color)  # type pygame.Surface
            self.text_rect = self.text_render.get_rect()  # type pygame.Rect
            self.W, self.H = self.text_rect.width, self.text_rect.height
            text_rect_LTpos = GraphUI.get_LT_by_LT_code_pos(LT_code_pos, L, T, self.W, self.H)
            self.text_rect.left, self.text_rect.top = text_rect_LTpos
            self.L, self.T = self.text_rect.left, self.text_rect.top
            v.screen.blit(self.text_render, self.text_rect)  # blit (Surface, Rect)
            if border:
                GraphUI.draw_rect(self.L, self.T, self.W, self.H, border_width=border_width,
                                  border_color=border_color)
            if event_id:
                GraphUI.handle_collide_events(self.text_rect, event_id)  # event handling

    # -------------------------------------------------------------------------------------------- #

    class ImageBox:
        """ Displays an image already loaded specified by its :img_id: on the screen at position
        (:L:, :T:). If the arguments are specified, it is also possible to specify the relative
        position code :LT_code_pos: (see docstring "get_LT_by_LT_code_pos"), the :event_id:,
        the presence of a :border:, and if so the :border_color: and the :border_width:.
        Attributes : L, T, W, H, img_render, img_rect. """

        """ Using a class provides access to attributes after image box display. """

        def __init__(self, img_id: str, L: int, T: int, LT_code_pos: str = 'CC',
                     event_id: str = '', border: str = False, border_color: tuple = c.RED,
                     border_width: int = 1, except_button: bool = False,
                     hover_img: bool = False, flip: bool = False) -> None:
            if hover_img and v.Events[event_id][0]:
                img_id += '_hover'
            assert img_id in v.Images, f'img_id invalid : {img_id}'
            self.img_render = v.Images[img_id]  # type pygame.Surface
            self.img_rect = self.img_render.get_rect()  # type pygame.Rect
            self.W, self.H = self.img_rect.width, self.img_rect.height
            img_rect_LTpos = GraphUI.get_LT_by_LT_code_pos(LT_code_pos, L, T, self.W, self.H)
            self.img_rect.left, self.img_rect.top = img_rect_LTpos
            self.L, self.T = self.img_rect.left, self.img_rect.top
            if flip:
                self.img_render = pygame.transform.flip(self.img_render, True, False)
            v.screen.blit(self.img_render, self.img_rect)  # blit (Surface, Rect)
            if border:
                GraphUI.draw_rect(self.L, self.T, self.W, self.H, border_width=border_width,
                                  color=border_color)
            if event_id:
                GraphUI.handle_collide_events(self.img_rect, event_id, except_button)
            if GraphUI.check_focus(event_id):
                GraphUI.draw_rect(self.L, self.T, self.W, self.H, 'TL', color=c.AMARANTH_PURPLE,
                                  border_width=10, border_radius_type='null')
                if v.focus_enter:
                    v.Events[event_id][1] = True
                    v.focus_enter = False

    # -------------------------------------------------------------------------------------------- #

    def draw_border(L: int, T: int, W: int, H: int, border_width: int = 1,
                    border_color: tuple = c.RED) -> None:
        """ Draws a border to the rectangle associated with the dimensions (:L:, :T:, :W:, :H:).
        Possible to specify <border_width> and <border_color>. """
        pygame.draw.lines(v.screen, border_color, True, [(L, T), (L+W, T), (L+W, T+H), (L, T+H)],
                          border_width)

    # -------------------------------------------------------------------------------------------- #

    def border_rect(args: tuple, br: int = 10, brt: str = 'all') -> pygame.Rect:
        """ :brt: all // left // right // top // bottom // TL // BL // TR // BR """
        if brt == 'all':
            return pygame.draw.rect(*args, border_radius=br)
        elif brt == 'left':
            return pygame.draw.rect(*args, border_top_left_radius=br,
                                    border_bottom_left_radius=br)
        elif brt == 'right':
            return pygame.draw.rect(*args, border_top_right_radius=br,
                                    border_bottom_right_radius=br)
        elif brt == 'top':
            return pygame.draw.rect(*args, border_top_left_radius=br,
                                    border_top_right_radius=br)
        elif brt == 'bottom':
            return pygame.draw.rect(*args, border_bottom_left_radius=br,
                                    border_bottom_right_radius=br)
        elif brt == 'TL':
            return pygame.draw.rect(*args, border_top_left_radius=br)
        elif brt == 'BL':
            return pygame.draw.rect(*args, border_bottom_left_radius=br)
        elif brt == 'TR':
            return pygame.draw.rect(*args, border_top_right_radius=br)
        elif brt == 'BR':
            return pygame.draw.rect(*args, border_bottom_right_radius=br)

    # -------------------------------------------------------------------------------------------- #

    def draw_rect(L: int, T: int, W: int, H: int, LT_code_pos: str = 'CC', event_id: str = '',
                  color: tuple = c.BLACK, alpha: int = 0, border_width: int = 0,
                  border_radius: int = 10, border_radius_type: str = 'all') -> pygame.Rect:
        """ Draws a rectangle of dimensions (:L:, :T:, :W:, :H:) with :LT_code_pos: relative
        position, with a :color: compatible to an :alpha: opacity. If a :border_width: is
        specified, rect will not be filled. You can also specify a :border_radius:, but note that
        :border_radius: isn't compatible with :alpha:. Event handling with :event_id:.
        :boder_radius_type: null // all // left // right // top // bottom //
        TL // BL // TR // BR """
        L, T = GraphUI.get_LT_by_LT_code_pos(LT_code_pos, L, T, W, H)
        if alpha:
            assert 0 <= alpha <= 1
            rect_surface = pygame.Surface((W, H)).convert_alpha()
            rect_surface.fill(pygame.Color(*color, round(alpha*255)))
            v.screen.blit(rect_surface, (L, T))
            GraphUI.draw_border(L, T, W, H, border_width, color)
            rect = rect_surface.get_rect()
        else:
            if border_radius_type == 'null':
                rect = pygame.draw.rect(v.screen, color, (L, T, W, H), border_width)
            else:
                rect = GraphUI.border_rect((v.screen, color, (L, T, W, H), border_width),
                                           border_radius, border_radius_type)
        if event_id:
            GraphUI.handle_collide_events(rect, event_id)  # event handling
        return rect

    # -------------------------------------------------------------------------------------------- #

    def draw_polygon(points: list, color: tuple = c.BLACK, alpha: int = 0, event_id: str = '',
                     border_width: int = 0) -> None:
        """ Draws a polygon whose dimensions are specified by a list of :points:, with a :color:
        compatible to an :alpha: opacity. If a :border_width: is specified, polygon will not be
        filled. Event handling with :event_id:. """
        if alpha:
            assert 0 <= alpha <= 1
            list_x, list_y = zip(*points)
            min_x, min_y, max_x, max_y = min(list_x), min(list_y), max(list_x), max(list_y)
            rect_surface = pygame.Rect(min_x, min_y, max_x-min_x, max_y-min_y)
            polygon_surface = pygame.Surface(rect_surface.size, pygame.SRCALPHA)
            pygame.draw.polygon(polygon_surface, pygame.Color(*color, round(alpha*255)),
                                [(x-min_x, y-min_y) for x, y in points], width=border_width)
            v.screen.blit(polygon_surface, rect_surface)
        else:
            polygon_surface = pygame.draw.polygon(v.screen, color, points, width=border_width)
        if event_id:
            GraphUI.handle_collide_events(polygon_surface, event_id)  # event handling

    # -------------------------------------------------------------------------------------------- #

    def draw_circle(L: int, T: int, color: tuple = c.BLACK, radius: int = 10, event_id: str = '',
                    border_width: int = 0) -> None:
        """ Draws a :color: circle of center (:L:, :T:) with R = :radius:. If a :border_width: is
        specified, circle will not be filled. Event handling with :event_id:. """
        circle_surface = pygame.draw.circle(v.screen, color, (L, T), radius, width=border_width)
        if event_id:
            GraphUI.handle_collide_events(circle_surface, event_id)  # event handling

    # -------------------------------------------------------------------------------------------- #

    def draw_line(start_pos: tuple, end_pos: tuple, color: tuple = c.BLACK,
                  border_width: int = 1) -> None:
        """ Draws a :border_width: and :color: straight line from :start_pos: point
        to :end_pos: point. """
        pygame.draw.line(v.screen, color, start_pos, end_pos, width=border_width)

    # -------------------------------------------------------------------------------------------- #

    def draw_lines(start_pos: tuple, end_pos: tuple, color: tuple = c.BLACK,
                   border_width: int = 1, auto_closed: bool = False) -> None:
        """ Draws a set of :border_width: and :color: straight lines specified with a :points: list
        of tuples (start_pos point, end_pos point). Can be :auto_closed:. """
        pygame.draw.line(v.screen, color, start_pos, end_pos, width=border_width,
                         closed=auto_closed)

    # -------------------------------------------------------------------------------------------- #

    def text_button(text: str, L: int, T: int, W: int, H: int, event_id: str,
                    LT_code_pos: str = 'CC', color: tuple = c.CADET_GRAY,
                    hover_color: tuple = c.MOONSTONE, active_color: tuple = c.AMARANTH_PURPLE,
                    border_color: tuple = c.DIM_GRAY, border_radius: int = 20,
                    border_width: int = 3, text_color: tuple = c.GUNMETAL,
                    text_size: int = 50) -> None:
        L, T = GraphUI.get_LT_by_LT_code_pos(LT_code_pos, L, T, W, H)
        if v.Events[event_id][0]:
            color = hover_color
        rect = GraphUI.draw_rect(L, T, W, H, 'TL', color=color, border_radius=border_radius)
        GraphUI.TextBox(text, L+W/2, T+H/2, size=text_size, color=text_color)
        if v.Active[event_id]:
            GraphUI.draw_rect(L+W/2, T+H/2, W, H, border_width=border_width,
                              border_radius=border_radius, color=active_color)
        elif v.Events[event_id][0]:
            GraphUI.draw_rect(L+W/2, T+H/2, W, H, border_width=border_width,
                              border_radius=border_radius, color=border_color)
        GraphUI.handle_collide_events(rect, event_id)  # event handling
        if GraphUI.check_focus(event_id):
            GraphUI.draw_rect(L, T, W, H, 'TL', color=c.AMARANTH_PURPLE, border_width=10,
                              border_radius_type='null')
            if v.focus_enter:
                v.Events[event_id][1] = True
                v.focus_enter = False

    # -------------------------------------------------------------------------------------------- #

    def wood_button(text: str, L: int, T: int, LT_code_pos: str = 'CC', event_id: str = '',
                    except_button: bool = False, little: bool = False) -> None:
        if v.Events[event_id][0]:
            button = GraphUI.ImageBox('wood_lil_button_hover' if little else 'wood_button_hover',
                                      L, T, LT_code_pos=LT_code_pos, event_id=event_id,
                                      except_button=except_button)
        else:
            button = GraphUI.ImageBox('wood_lil_button' if little else 'wood_button', L, T,
                                      LT_code_pos=LT_code_pos, event_id=event_id,
                                      except_button=except_button)
        L, T = button.L + button.W/2, button.T + button.H/2
        GraphUI.TextBox(text, L, T, size=25 if little else 50, color=c.PALE_DOGWOOD)

    # -------------------------------------------------------------------------------------------- #

    def slider(L: int, T: int, W: int, H: int, LT_code_pos: str = 'CC', slider_id: str = '',
               button_color: tuple = c.GUNMETAL, over_color: tuple = c.LIGHT_SLATE_GRAY,
               under_color: tuple = c.SLATE_GRAY, button_width: int = 5,
               mini: int = 0, maxi: int = 100, unit: str = '') -> int:
        L, T = GraphUI.get_LT_by_LT_code_pos(LT_code_pos, L, T, W, H)
        coef = v.SliderPos[slider_id]
        GraphUI.draw_rect(L, T, W, H, 'TL', color=under_color, event_id=slider_id, border_radius=7,
                          border_radius_type='all')
        GraphUI.draw_rect(L, T, coef*(W-button_width)+button_width/2, H, 'TL', color=over_color,
                          border_radius=7, border_radius_type='left')
        GraphUI.draw_rect(L+coef*(W-button_width), T, button_width, H, 'TL', color=button_color,
                          border_radius=7, border_radius_type='all')
        val = round(mini+coef*(maxi-mini-1)) if coef < 1 else round(maxi)
        GraphUI.TextBox(f'{val} {unit}'.strip(), L+W/2, T+H/2, size=40, color=c.WHITE)
        if v.Events[slider_id][1]:
            v.slider_move = slider_id
        if pygame.mouse.get_pressed()[0] != 0 and (v.MousePos.end_motion != c.DEF_POS) and \
                (v.slider_move == slider_id) and not v.wait_for_next_click:
            posx = pygame.mouse.get_pos()[0] - button_width/2
            posx = L if posx < L else (L+W if posx > L+W else posx)
            v.SliderPos[slider_id] = (posx-L)/W
        return val

    # -------------------------------------------------------------------------------------------- #

    def value_slider(L: int, T: int, W: int, H: int, value_slider_id: str,
                     bg_color: tuple = c.BLACK, unit: str = '',
                     disable: bool = False, freezevalue: int = 0) -> int or str:
        val = v.ValueSlider[value_slider_id][1][v.ValueSlider[value_slider_id][0]]
        GraphUI.draw_rect(L, T, W, H, color=bg_color)
        if not disable:
            GraphUI.TextBox(f'{val} {unit}'.strip(), L, T, color=c.WHITE, size=40)
            GraphUI.ImageBox('left_arrow_black', L-W/2+v.Images['left_arrow_black'].get_width()/2, T,
                             event_id='left_arrow', hover_img=True)
            GraphUI.ImageBox('right_arrow_black', L+W/2-v.Images['right_arrow_black'].get_width()/2, T,
                             event_id='right_arrow', hover_img=True)
        else:
            GraphUI.TextBox(f'{freezevalue} {unit}'.strip(), L, T, color=c.DIM_GRAY, size=40)
            GraphUI.ImageBox('left_arrow_dim_gray', L-W/2+v.Images['left_arrow_dim_gray'].get_width()/2, T)
            GraphUI.ImageBox('right_arrow_dim_gray', L+W/2-v.Images['right_arrow_dim_gray'].get_width()/2, T)
        if v.Events['left_arrow'][1]:
            v.ValueSlider[value_slider_id][0] -= 1
            if v.ValueSlider[value_slider_id][0] < 0:
                v.ValueSlider[value_slider_id][0] = len(v.ValueSlider[value_slider_id][1])-1
        if v.Events['right_arrow'][1]:
            v.ValueSlider[value_slider_id][0] += 1
            if v.ValueSlider[value_slider_id][0] >= len(v.ValueSlider[value_slider_id][1]):
                v.ValueSlider[value_slider_id][0] = 0
        return val

    # -------------------------------------------------------------------------------------------- #

    def check_focus(event_id):
        if v.subpage in v.focus_order and v.focus is not None:
            focus_group = v.focus_order[v.subpage]
            assert 0 <= v.focus < len(focus_group), 'focus overflow'
            return focus_group[v.focus] == event_id
        return False

    # -------------------------------------------------------------------------------------------- #

    def on_off_button(L: int, W: int, event_id: str) -> int:
        GraphUI.ImageBox(f'switch_button_{v.OnOff[event_id][1]+1}', L, W, event_id=event_id)
        if v.on_off_transition[event_id]:
            if v.OnOff[event_id][0] == 0:
                v.OnOff[event_id][1] += 1
                if v.OnOff[event_id][1] == v.on_off_range-1:
                    v.on_off_transition[event_id] = False
                    v.OnOff[event_id][0] = v.on_off_range-1
            elif v.OnOff[event_id][0] == v.on_off_range-1:
                v.OnOff[event_id][1] -= 1
                if v.OnOff[event_id][1] == 0:
                    v.on_off_transition[event_id] = False
                    v.OnOff[event_id][0] = 0
        if v.Events[event_id][1] and not v.on_off_transition[event_id]:
            v.on_off_transition[event_id] = True
        return v.OnOff[event_id][1] == v.on_off_range-1

    # -------------------------------------------------------------------------------------------- #

    def TextInput(L: int, T: int, W: int, H: int, field_id: str, value: str = '',
                  text_color: tuple = c.GUNMETAL) -> str:
        GraphUI.draw_rect(L, T, W, H, event_id=field_id, color=c.SILVER)
        t = GraphUI.TextBox(value, L, T, size=30, color=text_color)
        if v.Active[field_id]:
            GraphUI.draw_rect(L, T, W, H, border_width=5, border_radius=10,
                              color=c.AMARANTH_PURPLE)
            v.text_input = True
            v.text_overflow = t.W > W*3/4
        return value

# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
