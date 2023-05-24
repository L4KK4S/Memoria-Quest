""" Projet Transverse - Groupe A3 - Fichier cursor.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Python libraries
import pygame

# Internal modules
import variables as v


# ___________________________________________ CLASSES ____________________________________________ #


class Mouse():
    def __init__(self):
        super().__init__()
        self.rect = v.Images['cursor'].get_rect(topleft=(10, 10))
        self.mask = pygame.mask.from_surface(v.Images['cursor'])
        # Initialisation de la position de la souris
        self.rect.x = v.H/2
        self.rect.y = v.W/2

    def update_position(self):
        position = pygame.mouse.get_pos()  # Récupère la position de la souris
        self.rect.x = position[0] + v.camera.scroll_x  # Change position de la souris sur l'axe x
        self.rect.y = position[1] + v.camera.scroll_y  # Change position de la souris sur l'axe y


# ------------------------------------------------------------------------------------------------ #


class Cursor():
    def __init__(self, player):
        super().__init__()
        # Définit la position initiale et la taille du viseur
        self.rect = pygame.Rect(player.rect.centerx + v.camera.scroll_x,
                                v.H/2 + v.camera.scroll_y, 20, 20)
        self.player_x = player.rect.x

    def update_position(self, player):  # Modification de la position du viseur
        if 'viewfinder_up' in player.inputs:
            self.rect.y -= 7
        if 'viewfinder_down' in player.inputs:
            self.rect.y += 7
        if 'viewfinder_left' in player.inputs:
            self.rect.x -= 7
        if 'viewfinder_right' in player.inputs:
            self.rect.x += 7

        self.rect.x += (player.rect.x - self.player_x)  # Déplacement du viseur en fonction du joueur
        self.player_x = player.rect.x
        
        if player.last_direction == -1 and self.rect.x > player.rect.centerx:  # Limite le viseur si le joueur essaye de le passer derrière le personnages
            self.rect.x = player.rect.centerx
        elif player.last_direction == 1 and self.rect.x < player.rect.centerx:
            self.rect.x = player.rect.centerx


# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
