""" Projet Transverse - Groupe A3 - Fichier run.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Python libraries
import pygame

# Internal modules
from main import Main


# __________________________________________ FUNCTIONS ___________________________________________ #


def main():
    try:
        game = Main()
        game.run_game()
    finally:
        pygame.quit()
