""" Projet Transverse - Groupe A3 - Fichier bonus.py """


# ___________________________________________ IMPORTS ____________________________________________ #


from typing import Any
import pygame

import constants as c
import variables as v
import ux as x
import animations
import math
import random as r

# ___________________________________________ CLASSES ____________________________________________ #


# La super class enemy
class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # variables initiales pour les fonctions associés
        self.tick = 0


    def display(self) -> None:
        v.screen.blit(v.Images[f'{self.name}'], self.rect)

    def collision(self, player) -> bool:
        if pygame.sprite.spritecollide(self, v.Players_Group, False, pygame.sprite.collide_mask):
            return True
        
    def touch(self) -> None:
        
        for i, player in enumerate(pygame.sprite.spritecollide(self, v.Players_Group, False, pygame.sprite.collide_mask)):

            if self.name == 'life_potion':
                    player.lives += self.life_effect
                    self.active = False
                    break

            elif self.name == 'speed_potion':
                    player.speed += self.speed_effect
                    player.jump_force += self.jump_effect
                    self.player_index = i
                    self.timer = 1
                    self.rect.y = -1000

            elif self.name == 'power_potion':
                    player.damage *= self.power_effect
                    for enemy in v.Enemies_Group.sprites():
                        enemy.damage *= self.protection_effect
                    self.player_index = i
                    self.timer = 1
                    self.rect.y = -1000
        



class LifePotion(Bonus):

    def __init__(self, coordinates):
        super().__init__()

        # image et rect
        self.name = 'life_potion'
        self.dir = v.images_dir + 'bonus'
        self.image = v.Images[f'{self.name}']
        self.rect = self.image.get_rect(midbottom=coordinates)

        self.active = True
        self.life_effect = 3

    def update(self) -> None:
        
        self.touch()


class SpeedPotion(Bonus):

    def __init__(self, coordinates):
        super().__init__()

        # image et rect
        self.name = 'speed_potion'
        self.dir = v.images_dir + 'bonus'
        self.image = v.Images[f'{self.name}']
        self.rect = self.image.get_rect(midbottom=coordinates)

        self.player_index = -1
        self.active = True

        self.speed_effect = 3
        self.jump_effect = 5
        self.time_effect = 10 
        self.timer = 0

    def effect(self) -> None:
        
        if self.timer == v.FPS * self.time_effect:
            v.Players_Group.sprites()[self.player_index].speed -= self.speed_effect
            v.Players_Group.sprites()[self.player_index].jump_force -= self.jump_effect
            self.active = False

        if self.timer:
            self.timer += 1


    def update(self) -> None:
        
        self.touch()
        self.effect()


class PowerPotion(Bonus):

    def __init__(self, coordinates):
        super().__init__()

        # image et rect
        self.name = 'power_potion'
        self.dir = v.images_dir + 'bonus'
        self.image = v.Images[f'{self.name}']
        self.rect = self.image.get_rect(midbottom=coordinates)

        self.player_index = -1
        self.active = True

        self.power_effect = 2
        self.protection_effect = 0.5
        self.time_effect = 10 
        self.timer = 0

    def effect(self) -> None:
        
        if self.timer == v.FPS * self.time_effect:
            v.Players_Group.sprites()[self.player_index].damage /= self.power_effect
            for enemy in v.Enemies_Group.sprites():
                enemy.damage /= self.protection_effect
            self.active = False

        if self.timer:
            self.timer += 1


    def update(self) -> None:
        
        self.touch()
        self.effect()






# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
