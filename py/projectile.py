""" Projet Transverse - Groupe A3 - Fichier projectile.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Python libraries
import math
import pygame

# Internal modules
import variables as v
import constants as c


# __________________________________________ FUNCTIONS ___________________________________________ #


def shoot_angle(player):
    diff_y = player.viewfinder.rect.y - player.rect.y
    diff_x = player.viewfinder.rect.x - player.rect.centerx
    if diff_x == 0:
        diff_x = 1
    angle = math.atan(diff_y/diff_x)
    if diff_x < 0:
        angle = math.pi + angle
    return angle


def draw_projectile_path(player, speed):
    angle = shoot_angle(player)
    x = player.rect.centerx
    y = player.rect.y
    for i in range(1, 200):
        t = i/8
        x_i = speed*math.cos(angle) * t + player.rect.centerx
        y_i = (c.GRAVITY / 2) * t ** 2 + speed * math.sin(angle) * t + player.rect.y
        if i % 2:
            pygame.draw.line(v.screen, v.colors[player.name], (x - v.camera.scroll_x, y - v.camera.scroll_y),
                             (x_i - v.camera.scroll_x, y_i - v.camera.scroll_y), 3)
        x = x_i
        y = y_i


# ___________________________________________ CLASSES ____________________________________________ #


class Projectile(pygame.sprite.Sprite):

    def __init__(self, player, speed):
        super().__init__()
        self.rect = pygame.Rect(player.rect.x, player.rect.y, 10, 10)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.set_alpha(100)
        self.x_0 = player.rect.centerx
        self.y_0 = player.rect.y
        self.tick = pygame.time.get_ticks()
        self.speed = speed
        self.angle = shoot_angle(player)

    def shooting(self):
        self.t = (pygame.time.get_ticks() - self.tick) / 80
        self.rect.centerx = self.speed*math.cos(self.angle) * self.t + self.x_0
        self.rect.centery = (c.GRAVITY / 2) * self.t ** 2 + self.speed * math.sin(self.angle) * \
            self.t + self.y_0

    def collide_bloc(self, tilemap):
        for tile in tilemap:
            if self.rect.colliderect(tile.rect):
                return True
        return False

    def collide_enemy(self):
        for enemy in pygame.sprite.spritecollide(self, v.Enemies_Group, False, pygame.sprite.collide_mask):
            if enemy.state not in ['hit', 'death']:
                enemy.state = 'hit'
                enemy.frame = 1
                enemy.lives -= 1
                return True
        return False


# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
