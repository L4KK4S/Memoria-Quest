""" Projet Transverse - Groupe A3 - Fichier player.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Python libraries
import pygame

# Internal modules
import variables as v
import constants as c
import ux as x
import cursor
import projectile
import animations


# ___________________________________________ CLASSES ____________________________________________ #


class Player(animations.Animations):
    def __init__(self, coordinates, i):
        super().__init__()
        self.name = "player"
        self.dir = v.images_dir+'player'
        self.controller = None
        self.id_player = i
        self.controller_id = v.id_players[self.id_player]
        self.name = v.associated_names[v.player_choices[f'P{self.id_player + 1}']]
        self.rect = v.Images[f'{self.name}player_idle_1'].get_rect(midbottom=coordinates)
        self.mask = pygame.mask.from_surface(v.Images[f'{self.name}player_idle_1'])
        self.direction = pygame.math.Vector2(y=1)
        self.speed = 4
        self.dash_mult = 2  # multiplicateur appliqué à la vitesse lors d'un dash (sprint)
        self.jump_force = 50

        # Variables pour le tir à l'arc
        self.viewfinder = cursor.Cursor(self)  # Viseur
        self.shooting_arrow = False  # True si une flèche doit être tirée
        self.arrow_speed = 80  # Vitesse initiale de la flèche
        self.path_arrow = False  # True pour afficher la trajectoire de la flèche
        self.nb_arrow = 0  # Nombre de flèches
        self.arrows = []  # Liste des flèches attribuées au joueur

        self.tick = 0
        self.dash_cooldown = 1  # cooldown du dash du joueur en secondes
        self.tick_dash = pygame.time.get_ticks()  # temps depuis le dernier sprint
        self.tick_arrow = pygame.time.get_ticks()  # Temps depuis le dernier tir de flèche
        self.height = self.rect.y

        self.alive = True
        self.lives = v.nb_lives
        self.damage = 1
        self.hit = False
        self.hit_distance_coeff = 1.5
        self.recoil = 2
        self.look = "right"

        self.possible_animations = ['attack', 'attack-dash', 'combo', 'croutch', 'dash', 'death',
                                    'fall', 'hit', 'idle', 'jump', 'run', 'slide', 'throw']

        self.death_timer = 0

    def attack(self):
        # pour chaque ennemi touché
        for enemy in pygame.sprite.spritecollide(self, v.Enemies_Group, False, pygame.sprite.collide_mask):
            # si l'ennemi est bien placé
            if enemy.rect.centerx < self.rect.centerx and self.last_direction == -1 \
                    or enemy.rect.centerx > self.rect.centerx and self.last_direction == 1:
                if enemy.state not in ['hit', 'death']:
                    enemy.state = 'hit'
                    enemy.frame = 1
                    enemy.direction.x = self.last_direction
                    enemy.lives -= self.damage

    def player_shoot(self):
        if self.shooting_arrow:  # Vérifie si une flèche doit partir
            self.arrows.append(projectile.Projectile(self, self.arrow_speed))
            # Ajoute une flèche dans la liste des flèches du joueur
            self.nb_arrow += 1  # Augmente le nombre de flèches de 1
            self.shooting_arrow = False  # Dit que la flèche est déjà partie
        if self.nb_arrow:  # Vérifie si au minimum une flèche est en vol
            deleting = []  # Liste des indices des flèches à supprimer
            for i in range(self.nb_arrow):
                self.arrows[i].shooting()  # Actualise la position de la flèche
            if self.arrows[i].rect.y > 1080:  # Vérifie si la flèche est arrivée
                deleting.append(i)  # Met l'indice de la flèche dans la listes des flèches à supp
            deleting.reverse()  # Inverse la liste des indices
            for i in deleting:
                del(self.arrows[i])  # Supprime la flèche de la liste
                self.nb_arrow -= 1  # Diminue le nombre de flèches de 1

    def handle_input(self, inputs):

        self.tick_status = pygame.time.get_ticks()
        self.inputs = inputs
        self.viewfinder.update_position(self)
        if 'left' in self.inputs and 'right' not in inputs and self.state not in ['attack', 'combo', 'death',
                                                                                  'croutch', 'hit', 'throw']:
            self.direction.x = -1
            if self.last_direction != -1:
                self.viewfinder.rect.x -= 2 * (self.viewfinder.rect.x - self.rect.centerx)
            self.last_direction = -1
        elif 'right' in self.inputs and 'left' not in inputs and self.state not in ['attack', 'combo', 'death',
                                                                                    'croutch', 'hit', 'throw']:
            self.direction.x = 1
            if self.last_direction != 1:
                self.viewfinder.rect.x -= 2 * (self.viewfinder.rect.x - self.rect.centerx)
            self.last_direction = 1
        elif self.state != 'hit':
            self.direction.x = 0

        if 'down' in self.inputs and self.state != 'hit':
            if self.state == 'idle' and self.state != 'croutch':
                self.state = 'croutch'
                self.frame = 1
            elif self.state == 'run' and self.state != 'slide':
                self.state = 'slide'
                self.frame = 1

        if 'jump' in self.inputs and self.direction.y == 1 and self.state not in ['hit', 'death']:
            self.direction.y = -1
            self.tick = pygame.time.get_ticks()
            self.height = self.rect.y

        elif 'dash' in self.inputs and abs(self.tick_dash - pygame.time.get_ticks()) > self.dash_cooldown*1000 and self.direction.x != 0 \
                and self.state not in ['hit', 'death']:
            if self.state != 'dash':
                self.state = 'dash'
                self.frame = 1
                self.speed *= self.dash_mult

        elif 'attack' in self.inputs and self.state not in ['combo', 'hit', 'death']:
            pygame.mixer.Sound.play(v.Sounds['smash'])
            if self.state == 'attack' and self.frame == 6:
                self.state = 'combo'
                self.frame = 1
            elif self.state == 'dash':
                self.state = 'attack-dash'
                self.frame = 1
                self.speed /= self.dash_mult
            elif self.state == 'attack-dash' and self.frame >= 6:
                self.state = 'combo'
                self.frame = 1
            elif self.state not in ['attack', 'combo', 'attack-dash']:
                self.state = 'attack'
                self.frame = 1

        elif 'death' in self.inputs:  # a supprimer plus tard c'est pour test
            self.state = 'death'
            self.frame = 1
            self.death_timer = pygame.time.get_ticks()

        elif 'hit' in self.inputs:  # pareil c'est un test
            self.state = 'hit'
            self.frame = 1

        if 'shoot' in self.inputs and v.subpage == 'game_arcade' \
                and self.tick_status - self.tick_arrow > 1000:
            self.state = 'throw'
            self.frame = 1
            self.shooting_arrow = True  # Dit qu'une flèche attend d'être lancée
            self.tick_arrow = self.tick_status  # Réinitialise le compteur entre 2 flèches

        if 'arrow path' in self.inputs:
            self.path_arrow = True  # Active l'affichage de la trajectoire de la flèche
        else:
            self.path_arrow = False  # Désactive l'affichage de la trajectoire de la flèche
            
        if 'break' in self.inputs:
            v.subpage = 'break_'

        if not (self.state == 'throw' and self.frame < 4):
            self.player_shoot()  # Appel de la fonction de tir

        if self.state in ['attack', 'attack-dash', 'combo']:
            self.attack()

    def delete_arrow(self, arrow):
        self.arrows.remove(arrow)
        self.nb_arrow -= 1

# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
