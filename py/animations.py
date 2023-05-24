""" Projet Transverse - Groupe A3 - Fichier animations.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Python libraries
import os
import pygame

# Internal modules
import variables as v
from ui import GraphUI


# ___________________________________________ CLASSES ____________________________________________ #


class Animations(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.frame = 1
        self.timer = 0
        self.frequency = 90  # temps qui sépare deux images en ms
        self.last_direction = 1
        self.y_velocity = 0
        self.state = 'idle'
        self.possible_animations = []

    def animate(self, cam_x, cam_y):

        #print(self.y_velocity)
        if self.state not in ['attack', 'combo', 'hit', 'death', 'dash',
                              'attack-dash', 'croutch', 'slide', 'throw']:
            if self.y_velocity < -5 and 'jump' in self.possible_animations:
                if self.state != 'jump':
                    self.state = 'jump'
                    self.frame = 1
            elif self.y_velocity > 10 and 'fall' in self.possible_animations:
                if self.state != 'fall':
                    self.state = 'fall'
                    self.frame = 1
            elif self.direction.x == 0 and 'idle' in self.possible_animations:
                if self.state != 'idle':
                    self.state = 'idle'
                    self.frame = 1
            elif self.state not in ['run', 'jump'] and 'run' in self.possible_animations:
                self.state = 'run'
                self.frame = 1

        if self.name in ["Blue", "Green", "Red", "Purple"]:
            path = f'{self.name}player_{self.state}_{self.frame}'

        else:
            path = f'{self.name}_{self.state}_{self.frame}'

        if self.last_direction == 1:
            GraphUI.ImageBox(path,
                             self.rect.x - cam_x,
                             self.rect.y - cam_y,
                             'TL')
            self.mask = pygame.mask.from_surface(v.Images[path])
        else:
            GraphUI.ImageBox(path,
                             self.rect.x - cam_x,
                             self.rect.y - cam_y,
                             'TL',
                             flip=True)
            self.mask = self.flip_mask(v.Images[path])

        if pygame.time.get_ticks() - self.timer >= self.frequency:
            self.timer = pygame.time.get_ticks()
            self.frame += 1
            if self.frame > len(os.listdir(f'{self.dir}/{self.state}')):
                self.frame = 1
                if self.state in ['attack', 'combo', 'attack-dash', 'hit',
                                  'death', 'dash', 'croutch', 'slide', 'throw']:

                    if self.state == 'death':  # le cadavre disparait après après 10 sec
                        if (pygame.time.get_ticks() - self.death_timer > 5 * 10**3 or self.name == "Bringer-of-Death") \
                                and self.name not in ['Green', 'Blue', 'Red', 'Purple']:
                            self.kill()
                        else:
                            self.frame = len(os.listdir(f'{self.dir}/{self.state}'))
                    else:
                        if self.state == 'dash':
                            self.tick_dash = pygame.time.get_ticks()
                            self.speed /= self.dash_mult

                        self.state = 'idle'

    def flip_mask(self, surface):
        flipped = pygame.transform.flip(surface, True, False)
        flipped_mask = pygame.mask.from_surface(flipped)
        return flipped_mask


# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
