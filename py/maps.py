""" Projet Transverse - Groupe A3 - Fichier maps.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Python libraries
import pygame

# Internal modules
import variables as v
import constants as c
from player import Player
from ui import GraphUI
import projectile


# ___________________________________________ CLASSES ____________________________________________ #


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, tile_size, tile_type):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=position)
        self.id = self.get_id(tile_type)

    def get_id(self, n: int) -> str:
        return str(n-1).zfill(3)


# ------------------------------------------------------------------------------------------------ #


class MapHandler:
    def __init__(self):
        self.actual_map = None

    def update_actual_map(self):
        self.actual_map = self.set_map(v.Maps[f'{v.map_choice}'.capitalize()])

    def set_map(self, matrice_map):
        tiles_group = pygame.sprite.Group()
        for y in range(len(matrice_map)):
            for x in range(len(matrice_map[y])):
                if matrice_map[y][x] not in [-3, -2, -1, 0]:
                    pos = (x * c.TILE_SIZE, y * c.TILE_SIZE)
                    tiles_group.add(Tile(pos, c.TILE_SIZE, matrice_map[y][x]))
        return tiles_group

    def apply_gravity(self, sprite):

        dt = (pygame.time.get_ticks() - sprite.tick) / 80
        gravity = (c.GRAVITY / 2) * dt**2 + sprite.height
        if sprite.direction.y < 0:  # pour un saut
            sprite.y_velocity = round(c.GRAVITY * dt) - sprite.jump_force
            return gravity - sprite.jump_force * dt
        elif sprite.direction.y > -1:  # gravité
            sprite.y_velocity = round(c.GRAVITY * dt)
            return gravity

    def movement_collisions(self, sprite):

        # déplacement du l'axe y
        sprite.rect.y = self.apply_gravity(sprite)
        collide_box = self.set_collide_box(sprite)

        # si on touche un bloc suite à un déplacement vertical
        for tile in self.actual_map:
            if tile.rect.colliderect(collide_box):

                # collision en haut
                if sprite.direction.y < 0 and abs(collide_box[1]-tile.rect.bottom) < 20:
                    sprite.rect.top = tile.rect.bottom - (collide_box[1] - sprite.rect.y) + 5
                    sprite.direction.y = 0
                    sprite.tick = pygame.time.get_ticks()
                    sprite.height = sprite.rect.y
                    break

                else:
                    # collision au sol
                    sprite.rect.bottom = tile.rect.top
                    sprite.direction.y = 1
                    sprite.tick = pygame.time.get_ticks()
                    sprite.height = sprite.rect.y
                    if sprite.state == 'jump':
                        sprite.state = 'idle'

        # déplacement sur l'axe x
        if sprite.state == 'hit':
            sprite.rect.x += sprite.direction.x * sprite.recoil
        else:
            sprite.rect.x += sprite.direction.x * sprite.speed

        collide_box = self.set_collide_box(sprite)

        # si on touche un mur suite à un déplacement horizontal
        for tile in self.actual_map:
            if tile.rect.colliderect(collide_box):

                # collision à gauche
                if sprite.direction.x < 0:
                    if sprite.state == 'hit':
                        sprite.rect.x += sprite.recoil
                        collide_box[0] += sprite.recoil
                    else:
                        sprite.rect.x += sprite.speed
                        collide_box[0] += sprite.speed

                # collision à droite
                elif sprite.direction.x > 0:
                    if sprite.state == 'hit':
                        sprite.rect.x -= sprite.recoil
                        collide_box[0] -= sprite.recoil
                    else:
                        sprite.rect.x -= sprite.speed
                        collide_box[0] -= sprite.speed

                sprite.direction.x = 0

                if sprite.name not in ["Blue", "Green", "Red", "Purple", "Boar"] \
                        and sprite.direction.y == 1 \
                        and sprite.state != 'hit':
                    sprite.jump()

    def set_collide_box(self, sprite):
        collide_box = [sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height]
        collide_box[0] += collide_box[2] * 3/7
        collide_box[1] += collide_box[3] / 4 +1
        collide_box[2] = collide_box[2] / 7
        collide_box[3] = collide_box[3] * 3/4 -1
        return collide_box


# ------------------------------------------------------------------------------------------------ #


class Camera:
    def __init__(self, level: MapHandler):
        self.level = level
        self.camera_lag = 25
        self.scroll_x = 0
        # self.camera_scroll()
        self.scroll_y = 0

    def camera_scroll(self):
        average_coordinates = 0
        for player in v.Players_Group:
            average_coordinates += player.rect.x / v.nb_player
        self.scroll_x += (average_coordinates - self.scroll_x - v.W/2) // self.camera_lag
        if self.scroll_x < 0:
            self.scroll_x = 0
        right_border = len(v.Maps[f'{v.map_choice}'.capitalize()][0]) * 32
        if self.scroll_x + v.screen.get_width() > right_border:
            self.scroll_x = right_border - v.screen.get_width()


    def display(self):
        self.camera_scroll()
        # self.scroll_y += (self.player.rect.y - self.scroll_y - v.H / 2) // self.camera_lag - 10

        # Affichage des backgrounds
        for i in range(3):
            pos_x = int(-self.scroll_x * 0.3 * i) % v.W
            GraphUI.ImageBox(f'{v.map_choice}_bg{i+1}',
                             pos_x,
                             -self.scroll_y,
                             'TL')
            if pos_x > 0:
                pos_x -= v.W
            else:
                pos_x += v.W
            GraphUI.ImageBox(f'{v.map_choice}_bg{i+1}',
                             pos_x,
                             -self.scroll_y,
                             'TL')

        # Affichage des cases
        for tile in self.level.actual_map.sprites():
            GraphUI.ImageBox(f'map_tile{tile.id}',
                             tile.rect.x - self.scroll_x,
                             tile.rect.y - self.scroll_y,
                             'TL')

        
        
        # Affichage des ennemis
        for enemy in v.Enemies_Group:
            if enemy.name in ['Bringer-of-Death', 'Goblin', 'Boar']:
                enemy.animate(self.scroll_x, self.scroll_y)
                """contour_points = enemy.mask.outline()
                pygame.draw.lines(v.screen, (255, 0, 0), True, contour_points, 2)"""
            else:
                GraphUI.ImageBox(enemy.name,
                             enemy.rect.x - self.scroll_x,
                             enemy.rect.y - self.scroll_y,
                             'TL')
                
        # Affichage des bonus
        for bonus in v.Bonus_Group:
            GraphUI.ImageBox(bonus.name,
                             bonus.rect.x - self.scroll_x,
                             bonus.rect.y - self.scroll_y,
                             'TL')
            bonus.update()
                
        # Affichage des vies des joueurs
        for i, player in enumerate(v.Players_Group.sprites()):
            
            color = v.colors[player.name]
            font = pygame.font.Font(v.Fonts['default2'], 45)
            text = v.player_names[f'P{i+1}']
            text_render = font.render(text, True, color)
            v.screen.blit(text_render, (v.W // 2 - (text_render.get_width() * 1.3), 75 + text_render.get_height() * 1.1 * i))

            if player.lives > 0:
                lives = int(player.lives)
                half = True if (float(player.lives) - lives ) != 0 else False

                for j in range(lives):
                    v.screen.blit(v.Images['heart'], (v.W // 2 - v.Images['heart'].get_width() // 2 + v.Images['heart'].get_width() * j * 0.7, 75 + v.Images['heart'].get_height() * 1.1 * i))
                if half:
                    v.screen.blit(v.Images['half_heart'], (v.W // 2 - v.Images['heart'].get_width() // 2 + v.Images['half_heart'].get_width() * (lives) * 0.7, 75 + v.Images['half_heart'].get_height() * 1.1 * i))

            else:
                v.screen.blit(v.Images['skull'], (v.W // 2 - v.Images['skull'].get_width() // 2, 75 + v.Images['skull'].get_height() * 1.1 * i))
                player.alive = False

        

        # Affichage du joueur
        for player in v.Players_Group:
            """collide_box = [player.rect.x, player.rect.y, player.rect.width, player.rect.height]
            collide_box[0] += collide_box[2] * 3 / 7
            collide_box[1] += collide_box[3] / 4 + 1
            collide_box[2] = collide_box[2] / 7
            collide_box[3] = collide_box[3] * 3 / 4 - 1
            pygame.draw.rect(v.screen, 'red',
                             (collide_box[0] - self.scroll_x, collide_box[1],
                              collide_box[2], collide_box[3]))
            pygame.draw.rect(v.screen, 'blue',
                             [player.rect.x - self.scroll_x, player.rect.y - self.scroll_y,
                              player.rect.width, player.rect.height], 3)"""

            player.animate(self.scroll_x, self.scroll_y)

            # Affiche les flèches lancées par le joueur
            if player.nb_arrow:  # Vérifie s'il y a au minimum une flèche en vol
                for arrow in player.arrows:  # Affichage de la flèche
                    v.screen.blit(arrow.image, (
                    arrow.rect.x - self.scroll_x, arrow.rect.y - self.scroll_y, arrow.rect.width, arrow.rect.height))
                    pygame.draw.circle(v.screen, v.colors[player.name],
                                       (arrow.rect.centerx - self.scroll_x,
                                        arrow.rect.centery - self.scroll_y),
                                       7,2)
                    # vérifie si la flèche touche un mur ou un ennemi
                    if arrow.collide_bloc(self.level.actual_map) or arrow.collide_enemy():  # si un ennemi est touché, il perd de la vie
                        player.delete_arrow(arrow)
            """GraphUI.ImageBox('viewfinder',  # Affichage du viseur
                             player.viewfinder.rect.x - self.scroll_x,
                             player.viewfinder.rect.y - self.scroll_y,
                             'CC')"""
            if player.path_arrow:  # Vérifie si la trajectoire de la flèche doit s'afficher
                projectile.draw_projectile_path(player, player.arrow_speed)
                # Affichage de la trajectoire de la flèche


# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
