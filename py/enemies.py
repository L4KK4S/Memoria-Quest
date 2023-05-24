""" Projet Transverse - Groupe A3 - Fichier enemies.py """


# ___________________________________________ IMPORTS ____________________________________________ #


import pygame
import math
import datetime

import constants as c
import variables as v
import animations
import projectile
import math
import random as r

# ___________________________________________ CLASSES ____________________________________________ #

# La super class enemy
class Enemy(animations.Animations):
    def __init__(self):
        super().__init__()

        # variables initiales pour les fonctions associés
        self.tick = 0
        self.direction = pygame.math.Vector2()

        self.can_hit = True
        
        # initialisation de variables pour la gestion de la position du player
        self.player_at_left, self.player_at_right = False, False

        self.death_timer = 0

    def get_nearest_player(self):
        nearest = v.Players_Group.sprites()[0]
        distance = ((nearest.rect.centerx - self.rect.centerx)**2 + (nearest.rect.centery - self.rect.centery)**2) ** 0.5
        for player in v.Players_Group:
            if player.state != 'death':
                if ((player.rect.x - self.rect.centerx)**2 + (player.rect.centery - self.rect.centery)**2) ** 0.5 < distance:
                    nearest = player
                    distance = ((nearest.rect.centerx - self.rect.centerx)**2 + (nearest.rect.centery - self.rect.centery)**2) ** 0.5
        return nearest, distance
    
    def relative_player_position(self) -> None:

        # variables temporaires pour simplifier le code
        x = self.player.rect.centerx
        a = self.rect.centerx

        # verification de la position du player en x par rapport au sanglier
        if x < a:
            self.player_at_left = True
            self.player_at_right = False
        else:
            self.player_at_right = True
            self.player_at_left = False

    def jump(self) -> None:
        self.direction.y = -1
        self.tick = pygame.time.get_ticks()
        self.height = self.rect.y

    def hit(self) -> None:
        self.player.lives -= self.damage

# Le Boar est un ennemi terrestre, lent, il fait des dégats moyens qui repoussent l'adverse, il à un nombre moyen de points de vies, son ia de déplacement va à droite ou à gauche pour suivre le Player
class Boar(Enemy):

    def __init__(self, coordonnates):
        super().__init__()

        # image et rect
        self.name = 'Boar'
        self.dir = v.images_dir + 'enemies/Boar'
        self.image = v.Images[f'{self.name}_idle_1']
        self.rect = v.Images[f'{self.name}_idle_1'].get_rect(midbottom=coordonnates)
        self.height = self.rect.y
        self.player, self.distance = self.get_nearest_player()

        # stats du mob
        self.lives = self.player.damage * 4
        self.damage = 1.5
        self.speed = abs(r.randint(self.player.speed - 3, self.player.speed - 1))
        self.jump_force = 0
        self.recoil = 5

        # pour la position de spawn
        self.initial_x = self.rect.x
        self.height = self.rect.y
        self.is_initialized = True
        

        # pour la gestion du temps entre 2 charges
        self.hit_delay = 2
        self.last_hit = pygame.time.get_ticks()

        self.frequency = 150
        self.possible_animations = ['death', 'hit', 'idle', 'run']


    def movement(self) -> None:
        if self.distance < 500:

            if self.player.rect.centerx < self.rect.centerx - 20:
                self.direction.x = -1

            elif self.player.rect.centerx > self.rect.centerx + 20:
                self.direction.x = 1
            else:
                self.direction.x = 0

            # si le player est au dessus, ou en dessous, le sanglier ne bouge pas
            distance_y = abs(self.player.rect.centery - self.rect.centery)
            if abs(distance_y) > self.player.rect.height * 2:
                self.direction.x = 0

            # orientation de l'animation
            if self.player_at_left:
                self.last_direction = 1

            else:
                self.last_direction = -1

        else:
            self.direction.x = 0

    def attack(self) -> None:

        if self.can_hit:
            for player in pygame.sprite.spritecollide(self, v.Players_Group, False, pygame.sprite.collide_mask):
                if player.rect.centerx < self.rect.centerx and self.last_direction == 1 \
                        or player.rect.centerx > self.rect.centerx and self.last_direction == -1:
                    if player.state not in ['hit', 'dash', 'attack', 'combo', 'attack-dash', 'death']:
                        player.state = 'hit'
                        player.frame = 1
                        player.last_direction = self.last_direction
                        player.direction.x = -self.last_direction
                        self.hit()
                        self.can_hit = False

        # s'il a chargé, il ne bouge plus
        if not self.can_hit:
            self.direction.x = 0

        # gérer le compteur pour l'attente entre 2 charges
        if abs(self.last_hit - pygame.time.get_ticks()) > self.hit_delay*1000:
            self.last_hit = pygame.time.get_ticks()
            self.can_hit = True

    def update(self):

        if self.state == 'death':
            self.direction.x = 0

        elif self.state != 'hit':

            # récupère le player le plus proche s/o Adrian
            self.player, self.distance = self.get_nearest_player()

            # recupere les infos de la position du player
            self.relative_player_position()

            # si'il est placé au bon endroit, il bouge
            if self.is_initialized:
                self.movement()

            # systeme de coups donnés/reçus
            self.attack()

            # pour placer le sanglier au bon endroit
            if self.direction.y != 1 and not self.is_initialized:
                self.rect.x = self.initial_x
                self.is_initialized = True


# Le Goblin est un ennemi terrestre, rapide, mais qui fait peu de dégats,
# et qui a peu de points de vie
class Goblin(Enemy):

    def __init__(self, coordinnates):
        super().__init__()
        
        # image et rect
        self.name = 'Goblin'
        self.dir = v.images_dir+'enemies/Goblin'
        self.image = v.Images[f'{self.name}_idle_1']
        self.rect = v.Images[f'{self.name}_idle_1'].get_rect(midbottom=coordinnates)
        self.height = self.rect.y
        self.player, self.distance = self.get_nearest_player()

        # stats du mob
        self.lives = self.player.damage * 3  
        self.damage = 0.5
        self.speed = abs(r.randint(self.player.speed-1, self.player.speed))
        self.jump_force = 60
        self.recoil = 4

        # pour la position de spawn
        self.initial_x, self.height = self.rect.topleft
        self.is_initialized = False

        # pour la gestion du temps entre 2 charges (en secondes)
        self.hit_delay = 1.5
        self.counter = 0      
        self.can_hit = True
        self.last_hit = pygame.time.get_ticks()

        self.possible_animations = ['attack', 'death', 'hit', 'idle', 'run']

    def movement(self) -> None:
        if self.distance < 500 and self.state != 'attack':
            # si le player est à gauche, le goblin va à gauche, il s'arrete s'il est à une certaine distance
            if self.distance < 50:
                if self.state not in ['attack'] \
                        and abs(self.last_hit - pygame.time.get_ticks()) > self.hit_delay * 1000:
                    self.last_hit = pygame.time.get_ticks()
                    self.state = 'attack'
                    self.frame = 1
                else:
                    self.direction.x = 0
            elif self.player.rect.centerx < self.rect.centerx - 20:
                self.direction.x = -1

            elif self.player.rect.centerx > self.rect.centerx + 20:
                self.direction.x = 1
            else:
                self.direction.x = 0

            # si le player est au dessus, ou en dessous, le goblin ne bouge pas
            distance_y = abs(self.player.rect.centery - self.rect.centery)
            if abs(distance_y) > self.player.rect.height * 2:
                self.direction.x = 0

            # orientation de l'animation
            if self.player_at_left:
                self.last_direction = -1

            else:
                self.last_direction = 1

        else:
            self.direction.x = 0

    def attack(self) -> None:
        if self.can_hit and 5 <= self.frame <= 6:
            for player in pygame.sprite.spritecollide(self, v.Players_Group, False, pygame.sprite.collide_mask):
                if player.rect.centerx < self.rect.centerx and self.last_direction == -1 \
                        or player.rect.centerx > self.rect.centerx and self.last_direction == 1:
                    if player.state not in ['hit', 'dash', 'attack', 'combo', 'attack-dash', 'death']:
                        # ne met pas l'animation 'hit' du joueur car l'attaque est trop faible
                        self.hit()
                        self.can_hit = False

    def update(self) -> None:

        if self.state == 'death':
            self.direction.x = 0

        elif self.state != 'hit':
            # récupère le player le plus proche s/o Adrian
            self.player, self.distance = self.get_nearest_player()

            # recupere les infos de la position du player
            self.relative_player_position()

            # si'il est placé au bon endroit, il bouge
            if self.is_initialized:
                self.movement()

            # systeme de coups donnés/reçus
            if self.state == 'attack':
                self.attack()
            elif not self.can_hit:
                self.can_hit = True

            # pour placer le goblin au bon endroit
            if self.direction.y != 1 and not self.is_initialized:
                self.rect.x = self.initial_x
                self.is_initialized = True


class BringerofDeath(Enemy):

    def __init__(self, coordinnates):
        super().__init__()

        self.name = 'Bringer-of-Death'
        self.dir = v.images_dir+'enemies/Bringer_of_death'
        self.image = v.Images[f'{self.name}_idle_1']
        self.rect = v.Images[f'{self.name}_idle_1'].get_rect(midbottom=coordinnates)
        self.height = self.rect.y
        self.player, self.distance = self.get_nearest_player()

        self.speed = 2
        self.jump_force = 50
        self.lives = self.player.damage * 6
        self.damage = 1.5
        self.recoil = 4

        self.hit_delay = 3
        self.last_hit = pygame.time.get_ticks()

        self.frequency = 120
        self.possible_animations = ['attack', 'death', 'hit', 'idle', 'run', 'special']

    def movement(self):
        if self.distance < 500 and self.state != 'attack':
            if self.distance < 120:
                if self.state not in ['attack'] \
                        and abs(self.last_hit - pygame.time.get_ticks()) > self.hit_delay*1000:
                    self.last_hit = pygame.time.get_ticks()
                    self.state = 'attack'
                    self.frame = 1
                else:
                    self.direction.x = 0
            elif self.player.rect.centerx < self.rect.centerx-50:
                self.direction.x = -1

            elif self.player.rect.centerx > self.rect.centerx+50:
                self.direction.x = 1
            else:
                self.direction.x = 0

            if self.player_at_left:
                self.last_direction = 1

            else:
                self.last_direction = -1
        else:
            self.direction.x = 0

    def attack(self):
        if self.can_hit and 5 <= self.frame <= 7:
            for player in pygame.sprite.spritecollide(self, v.Players_Group, False, pygame.sprite.collide_mask):
                if player.rect.centerx < self.rect.centerx and self.last_direction == 1 \
                        or player.rect.centerx > self.rect.centerx and self.last_direction == -1:
                    if player.state not in ['hit', 'dash', 'attack', 'combo', 'attack-dash', 'death']:
                        player.state = 'hit'
                        player.frame = 1
                        player.last_direction = self.last_direction
                        player.direction.x = -self.last_direction
                        self.hit()
                        self.can_hit = False

    def update(self):
        if self.state == 'death':
            self.direction.x = 0
        elif self.state != 'hit':
            self.player, self.distance = self.get_nearest_player()
            self.relative_player_position()
            self.movement()
            if self.state == 'attack':
                self.attack()
            elif not self.can_hit:
                self.can_hit = True


# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
