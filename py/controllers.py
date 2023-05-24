""" Projet Transverse - Groupe A3 - Fichier controllers.py """


# ___________________________________________ IMPORTS ____________________________________________ #


# Libraires Python
import pygame

# Modules internes
import variables as v
import constants as c


# __________________________________________ FUNCTIONS ___________________________________________ #


def get_xbox_controller(controller: pygame.joystick.Joystick) -> dict:
    """
        Fonction qui permet de récupérer les entrées d'une manette de type Xbox
    """
    return {0: controller.get_button(2),  # bouton gauche
            1: controller.get_button(1),  # bouton droite
            'jump': controller.get_button(3),  # bouton haut
            'down': controller.get_button(0),  # bouton bas
            2: controller.get_button(6),  # bouton menu gauche
            'break': controller.get_button(7),  # bouton menu droite
            3: controller.get_button(10),  # bouton menu
            4: controller.get_button(8),  # clic joystick gauche
            5: controller.get_button(9),  # clic joystick droit
            'attack': controller.get_button(4),  # gachette L1
            'shoot': controller.get_axis(4) not in [-1, 0],  # gachette L2
            6: controller.get_button(5),  # gachette R1
            'arrow path': controller.get_axis(5) not in [-1, 0],  # gachette R2
            'left': controller.get_hat(0)[0] == -1 or controller.get_axis(0) < -0.3,  # flèche/joy.L gauche
            'right': controller.get_hat(0)[0] == 1 or controller.get_axis(0) > 0.3,  # flèche/joy.L droit
            7: controller.get_hat(0)[1] == 1 or controller.get_axis(1) < -0.3,  # flèche/joy.L haut
            8: controller.get_hat(0)[1] == -1 or controller.get_axis(1) > 0.3,  # flèche/joy.L bas
            'viewfinder_left': controller.get_axis(2) < -0.3,  # joy.R gauche
            'viewfinder_right': controller.get_axis(2) > 0.3,  # joy.R droit
            'viewfinder_up': controller.get_axis(3) < -0.3,  # joy.R haut
            'viewfinder_down': controller.get_axis(3) > 0.3}  # joy.R bas


def get_ps_controller(controller: pygame.joystick.Joystick) -> dict:
    """
        Fonction qui permet de récupérer les entrées d'une manette de type PlayStation
    """
    return {0: controller.get_button(2),  # bouton gauche
            1: controller.get_button(1),  # bouton droit
            'jump': controller.get_button(3),  # bouton haut
            'down': controller.get_button(0),  # bouton bas
            2: controller.get_button(4),  # bouton menu gauche
            'break': controller.get_button(6),  # bouton menu droit
            3: controller.get_button(5),  # bouton menu
            4: controller.get_button(7),  # clic joystick gauche
            5: controller.get_button(8),  # clic joystick droit
            'attack': controller.get_button(9),  # gachette L1
            'shoot': controller.get_axis(4) not in [-1, 0],  # gachette L2
            6: controller.get_button(10),  # gachette R1
            'arrow path': controller.get_axis(5) not in [-1, 0],  # gachette R2
            'left': controller.get_button(13) or controller.get_axis(0) < -0.3,  # flèche/joy.R gauche
            'right': controller.get_button(14) or controller.get_axis(0) > 0.3,  # flèche/joy.R droit
            7: controller.get_button(11) or controller.get_axis(1) < -0.3,  # flèche/joy.R haut
            8: controller.get_button(12) or controller.get_axis(1) > 0.3,  # flèche/joy.R bas
            'viewfinder_left': controller.get_axis(2) < -0.3,  # joy.L gauche
            'viewfinder_right': controller.get_axis(2) > 0.3,  # joy.L droit
            'viewfinder_up': controller.get_axis(3) < -0.3,  # joy.L haut
            'viewfinder_down': controller.get_axis(3) > 0.3}  # joy.l bas


def get_nintendo_controller(controller: pygame.joystick.Joystick) -> dict:
    """
        Fonction qui permet de récupérer les entrées d'une manette de type Nintendo Switch
    """
    return {0: controller.get_button(3),  # bouton gauche
            1: controller.get_button(0),  # bouton droit
            'jump': controller.get_button(2),  # bouton haut
            'down': controller.get_button(1),  # bouton bas
            2: controller.get_button(4),  # bouton menu gauche
            'break': controller.get_button(6),  # bouton menu droit
            3: controller.get_button(5),  # bouton menu
            4: controller.get_button(7),  # clic joystick gauche
            5: controller.get_button(8),  # clic joystick droit
            'attack': controller.get_button(9),  # gachette L1
            'shoot': controller.get_axis(4) not in [-1, 0],  # gachette L2
            6: controller.get_button(10),  # gachette R1
            'arrow path': controller.get_axis(5) not in [-1, 0],  # gachette R2
            'left': controller.get_button(13) or controller.get_axis(0) < -0.3,  # flèche/joy.R gauche
            'right': controller.get_button(14) or controller.get_axis(0) > 0.3,  # flèche/joy.R droit
            7: controller.get_button(11) or controller.get_axis(1) < -0.3,  # flèche/joy.R haut
            8: controller.get_button(12) or controller.get_axis(1) > 0.3,  # flèche/joy.R bas
            'viewfinder_left': controller.get_axis(2) < -0.3,  # joy.L gauche
            'viewfinder_right': controller.get_axis(2) > 0.3,  # joy.L droit
            'viewfinder_up': controller.get_axis(3) < -0.3,  # joy.L haut
            'viewfinder_down': controller.get_axis(3) > 0.3}  # joy.L bas


def get_actions(dict_actions: dict) -> list:
    """
        Fonction qui permet de convertir les dictionnaire des entrée manettes en une liste de commandes
    """
    return [i for i in dict_actions.keys() if dict_actions[i]]


def clavier() -> list:
    """
        Fonction qui permet de récupérer les entrées clavier
    """
    key_pressed = pygame.key.get_pressed()  # Récupère l'ensemble des entrées au clavier
    L = []  # Liste des id des entrées clavier
    T = []  # Liste des commandes du joueur
    for i in range(len(key_pressed)):
        if key_pressed[i]:  # Vérifie si la touche d'id i est pressée
            L.append(i)  # Ajoute l'id à la liste
    for i in c.COMMANDS.keys():
        if c.COMMANDS[i] in L:  # Vérifie si l'id est correspond à une commande du joueur
            T.append(i)  # Ajoute la commande à la liste des commandes
    return T  #Retourne la liste des commandes


def get_inputs_players(player):
    """
        Fonction qui permet de choisir la bonne entrée de commandes
    """
    if player.controller is None:  # V2rifie si l'id manette du joueur correspond au clavier
        inputs = clavier()  # Appelle de la fonction correspondant au clavier
    elif 'Nintendo' in player.controller.get_name():  # Vérifie s'il s'agit d'une manette Nintendo
        inputs = get_actions(get_nintendo_controller(player.controller))  # Appelle de la fonction correspondant à une manette Nintendo
    elif 'PS' in player.controller.get_name():  # Vérifie s'il s'agit d'une manette PlayStation
        inputs = get_actions(get_ps_controller(player.controller))  # Appelle de la fonction correspondant à une manette PlayStation
    else:  # Renvoie sur la mennette par défault (Xbox)
        inputs = get_actions(get_xbox_controller(player.controller))  # Appelle de la fonction correspondant à une manette Xbox
    player.handle_input(inputs)  # Appelle la fonction qui permet d'actualiser le joueur
    

def menu_controllers(id_player):
    """
        Fonction qui permet de vérifier quelle manette est en action dans le menu controllers
    """
    inputs = []  # Liste des entrées
    if v.id_players[id_player] == -1:  # Vérifie si l'id manette du joueur correspond au clavier
        keys = pygame.key.get_pressed()  # Récupère l'ensemble des entrées au clavier
        for i in range(len(keys)):
            if keys[i]:  # Vérifie si la touche d'id i est appuyée
                inputs.append(i)  # Ajoute l'id de la touche à la liste des actions
    elif 'Nintendo' in v.controllers[v.id_players[id_player]].get_name():  # Vérifie s'il s'agit d'une manette Nintendo
        inputs = get_actions(get_nintendo_controller(v.controllers[v.id_players[id_player]]))  # Appelle de la fonction correspondant à une manette Nintendo
    elif 'PS' in v.controllers[v.id_players[id_player]].get_name():  # Vérifie s'il s'agit d'une manette PlayStation
        inputs = get_actions(get_ps_controller(v.controllers[v.id_players[id_player]]))  # Appelle de la fonction correspondant à une manette PlayStation
    else:  # Renvoie sur la mennette par défault (Xbox)
        inputs = get_actions(get_xbox_controller(v.controllers[v.id_players[id_player]]))  # Appelle de la fonction correspondant à une manette Xbox
    if v.id_players[id_player] != -1:
        pygame.joystick.Joystick(v.id_players[id_player])  # Initialise chaque manette branchée
    v.actions_players[id_player] = inputs  # Ajoute la liste des entrées à la matrice des actions du joueur


def disconnected_controller():
    """
        Fonction qui permet de vérifier si une manette a été débranchée
    """
    return v.nb_controllers != pygame.joystick.get_count()  # Retourne 1 si une ou plusieurs manettes ont été débranchées


def connect_controllers(): 
    """
        Fonction qui permet de reconnecter dans la bon ordre les manettes débranchées
    """
    list = [None]  # Liste des manettes connectées
    for i in range(v.nb_controllers):
        list.append(pygame.joystick.Joystick(i))  #Ajoute à la liste les mannettes connectées
    i = 0
    for player in v.Players_Group:
        if player.controller_id != -1:  # Vérifie si l'id manettes du joueur ne correspond pas au clavier
            try:
                v.id_players[i] = list.index(player.controller) - 1  # Donnne au joueur son nouvel id manette si la manettes n'a pas été déconnectée
            except ValueError:
                v.id_players[i] = v.nb_controller - 1  # Donne au joueur l'id de la manette rebranchée
            if v.id_players[i] == v.nb_player:  # Sécurité au cas où il y aurait un décalage dans les id manettes
                v.id_players[i] = 0
            player.controller_id = v.id_players[i]  # Modifie l'id manette du joueur
            player.controller = pygame.joystick.Joystick(player.controller_id)  # Modifie la manette du joueur
        i += 1


# _____________________________________________ MAIN _____________________________________________ #


if __name__ == '__main__':
    import run
    run.main()
