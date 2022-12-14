from pygame_button import Button
import pygame
import pygame_textinput
import textwrap
from pygame.locals import *
import blackjack
from interface import Display, Cartes

# --MODULES--#


# Prépares les valeurs
game_running = True
pygame.font.init()
display = Display()
cartes = Cartes()
text_input = pygame_textinput.TextInputVisualizer(font_object=display.default_font,
                                                  font_color=(255, 255, 255), cursor_color=(255, 255, 255))
players_pos = []


def setup():
    """
    :return: Nombre de joueurs
    Demande le nombre de joueurs à l'utilisateur.
    """
    global players_pos
    setup_nbr_manager = pygame_textinput.TextInputManager(
        validator=lambda inp: len(inp) < 2 and inp.isnumeric() and int(inp) > 1)
    setup_nbr_input = pygame_textinput.TextInputVisualizer(manager=setup_nbr_manager, font_object=display.default_font,
                                                           font_color=(255, 255, 255), cursor_color=(255, 255, 255))

    while True:
        # Affiche le menu pour sélectionner le nombre de joueurs.
        display.board()

        name_text = display.huge_font.render("PyJackGame", False, (255, 255, 255))
        display.screen.blit(name_text, (name_text.get_rect(center=(display.h / 2, 0))[0], name_text.get_rect().centery))

        setup_nbr_input.update(display.pg_events)
        display.screen.blit(setup_nbr_input.surface, (display.screen.get_rect().centerx, display.w / 2))

        text = display.small_font.render("Entrez le nombre de joueurs (vous y compris): ", False, (255, 255, 255))
        display.screen.blit(text, (
            display.h / 2 - text.get_rect().centerx, display.w / 2 - display.default_font.get_height()))

        confirm_text = display.ultra_small_font.render("Appuyez sur Entrer pour confirmer", False, (210, 210, 210))
        display.screen.blit(confirm_text, (confirm_text.get_rect(center=(display.h / 2, display.w / 1.75))))

        display.update()  # Actualise l'interface
        for event in display.pg_events:
            if event.type == KEYDOWN:
                if event.key == pygame.K_BACKSPACE:  # Effacer si appuie sur effacer.
                    setup_nbr_input.value = ""
                if event.key in [pygame.K_KP_ENTER, pygame.K_RETURN]:  # Si l'utilisateur appuie sur Entrer
                    if setup_nbr_input.value != "":  # Vérifie si un nombre à bien était mis.
                        display.reset_error()
                        rad_jrs = 2 / int(setup_nbr_input.value)  # Prépare la position des cartes des joueurs.
                        for jrs in range(int(setup_nbr_input.value)):  # Je l'ai fait sans tuto, je me suis juste
                            players_pos.append(     # rappelé de mes cours spé math, je suis fier.
                                cartes.trigo_calc(rad_jrs * (jrs * 3.1), 310, (display.h / 2.5, display.w / 2.5)))

                        return int(setup_nbr_input.value)

                    else:  # Si l'utilisateur n'a rien écrit, afficher l'erreur.
                        display.error = "Erreur: Mettez un chiffre."


def as_func(joueur: int):
    """
        :param joueur: Le numéro de joueur
        :return: 1 ou 11 selon le choix du joueur
        Fonction si un joueur pioche un AS, peux choisir entre 1 et 11.
    """
    if joueur == 0:  # Si c'est l'utilisateur, afficher l'interface
        # Prépare les boutons
        button_1 = Button((display.w / 3, display.h / 2, 50, 60), (150, 150, 150), lambda a: a)
        button_1.process_kwargs({"text": display.small_font.render("1", False, (255, 255, 255)),
                                 "hover_color": (200, 200, 200)})
        button_11 = Button((display.w / 1.5, display.h / 2, 50, 60), (150, 150, 150), lambda a: a)
        button_11.process_kwargs({"text": display.small_font.render("11", False, (255, 255, 255)),
                                  "hover_color": (200, 200, 200)})
        while True:
            # Affiche l'interface pour choisir.
            display.board()

            for nbr, card in enumerate(game.j_perm_cards[0]):  # Affiche les cartes du joueur.
                display.screen.blit(cartes.cards[list(card.keys())[0]][list(card.values())[0]],
                                    (display.w / 3 + nbr * 20, display.w / 1.3))

            pygame.draw.rect(display.screen, (100, 100, 100),
                             (display.w / 3.6, display.h / 4.1, display.w / 1.935, display.h / 2.9))
            pygame.draw.rect(display.screen, (150, 150, 150),
                             (display.w / 3.5, display.h / 4, display.w / 2, display.h / 3))
            display.screen.blit(display.small_font.render("Vous avez récupéré un AS.", False,
                                                          (255, 255, 255)), (display.w / 3.2, display.h / 3.5))
            display.screen.blit(display.ultra_small_font.render("Voulez vous l'utiliser comme 1 ou 11?", False,
                                                                (255, 255, 255)), (display.w / 3.1, display.h / 3))
            button_1.update(display.screen)
            button_11.update(display.screen)

            display.update()

            for event in display.pg_events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Vérifie le choix.
                    if button_1.rect.collidepoint(event.pos):
                        return 1
                    if button_11.rect.collidepoint(event.pos):
                        return 11

    else:  # Fait un choix automatique si ce n'est pas l'utilisateur.
        if game.players_result[joueur] <= 10:
            return 11
        else:
            return 1


def retire_func(joueur):
    """
        :param joueur: Le numéro de joueur
        :return: True ou False selon le choix du joueur
        Fonction si un joueur à plus de 16, s'il veut s'arrêter.
    """
    if joueur == 0:  # Si c'est l'utilisateur, afficher l'interface
        # Prépare les boutons
        button_oui = Button((display.w / 3, display.h / 2, 75, 60), (150, 150, 150), lambda a: a)
        button_oui.process_kwargs({"text": display.small_font.render("Oui", False, (255, 255, 255)),
                                   "hover_color": (200, 200, 200)})
        button_non = Button((display.w / 1.5, display.h / 2, 75, 60), (150, 150, 150), lambda a: a)
        button_non.process_kwargs({"text": display.small_font.render("Non", False, (255, 255, 255)),
                                   "hover_color": (200, 200, 200)})
        while True:
            # Affiche l'interface pour choisir
            display.board()

            for nbr, card in enumerate(game.j_perm_cards[0]):  # Affiche les cartes du joueur.
                display.screen.blit(cartes.cards[list(card.keys())[0]][list(card.values())[0]],
                                    (display.w / 3 + nbr * 20, display.w / 1.3))

            pygame.draw.rect(display.screen, (100, 100, 100),
                             (display.w / 3.6, display.h / 4.1, display.w / 1.935, display.h / 2.9))
            pygame.draw.rect(display.screen, (150, 150, 150),
                             (display.w / 3.5, display.h / 4, display.w / 2, display.h / 3))
            display.screen.blit(display.small_font.render("Vous avez plus de 16.", False,
                                                          (255, 255, 255)), (display.w / 3.2, display.h / 3.5))
            display.screen.blit(display.ultra_small_font.render("Voulez-vous vous arrêter?", False,
                                                                (255, 255, 255)), (display.w / 3.1, display.h / 3))
            button_oui.update(display.screen)
            button_non.update(display.screen)

            display.update()

            for event in display.pg_events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Vérifie le choix.
                    if button_oui.rect.collidepoint(event.pos):
                        return True
                    if button_non.rect.collidepoint(event.pos):
                        return False
    else:
        if game.players_result[joueur] > 17:  # Fait un choix automatique si ce n'est pas l'utilisateur.
            return True
        else:
            return False


if "__main__" == __name__:
    # Crée le système de jeu.
    nbr_jrs = setup()
    game = blackjack.BlackJackGame(nbr_jrs)
    reveal = False
    ok = True

    # Prépare les boutons pour passer le tour et rejouer.
    button_ok = Button((display.w / 2.4, display.h / 2, 190, 60), (150, 150, 150), lambda a: a)
    button_ok.process_kwargs({"text": display.small_font.render("Tour suivant", False, (255, 255, 255)),
                              "hover_color": (200, 200, 200)})
    button_rematch = Button((display.w / 2.1, display.h / 1.8, 190, 60), (150, 150, 150), lambda a: a)
    button_rematch.process_kwargs({"text": display.small_font.render("Rejouer?", False, (255, 255, 255)),
                                   "hover_color": (200, 200, 200)})

    while True:  # En jeu
        display.board()

        for ply_cards in game.j_perm_cards:  # Affiche toutes les cartes de tous les jours (caché si pas l'utilisateur)
            for nbr, card in enumerate(game.j_perm_cards[ply_cards]):
                if ply_cards == 0 or reveal:
                    display.screen.blit(cartes.cards[list(card.keys())[0]][list(card.values())[0]],
                                        (players_pos[ply_cards][0] + nbr * 20, players_pos[ply_cards][1]))
                else:
                    display.screen.blit(cartes.cards["Reversed"][0],
                                        (players_pos[ply_cards][0] + nbr * 20, players_pos[ply_cards][1]))
        for x in range(game.cards_remaining):  # Affiche les cartes (cachés) qui reste.
            display.screen.blit(cartes.cards["Reversed"][1],
                                (display.w / 2.2 - cartes.cards["Reversed"][1].get_rect()[0] / 2.3 + x * 3,
                                 display.h / 2.7 - cartes.cards["Reversed"][1].get_rect()[1] / 2))
        display.screen.blit(display.small_font.render("Vous:", False, (255, 255, 255)),
                            (players_pos[0][0], players_pos[0][1] - 35))

        if game.cards_remaining == 0 or game.j_cards == {}:  # Si le matche est terminé.
            winners, losers = game.get_score()

            reveal = True  # Permet d'afficher les cartes des autres joueurs.
            pygame.draw.rect(display.screen, (100, 100, 100),
                             (display.w / 2.9, display.h / 3.1, display.w / 1.935, display.h / 2.9))
            pygame.draw.rect(display.screen, (150, 150, 150),
                             (display.w / 2.85, display.h / 3.05, display.w / 2, display.h / 3))
            display.screen.blit(display.default_font.render("Terminé!", True, (255, 255, 255)),
                                (display.w / 2, display.h / 4))

            if len(winners) > 1:  # Vérifie si plusieurs gagnants / perdants.
                display.screen.blit(display.small_font.render("Gagnants:", False, (255, 255, 255)),
                                    (display.w / 2.6, display.h / 2.8))
            elif len(winners) == 1:
                display.screen.blit(display.small_font.render("Gagnant:", False, (255, 255, 255)),
                                    (display.w / 2.6, display.h / 2.8))
            if len(losers) > 1:
                display.screen.blit(display.small_font.render("Perdants:", False, (255, 255, 255)),
                                    (display.w / 2.6, display.h / 2.4))
            elif len(losers) == 1:
                display.screen.blit(display.small_font.render("Perdants:", False, (255, 255, 255)),
                                    (display.w / 2.6, display.h / 2.4))

            if 0 in winners:
                winners.remove(0)
                winners.append("0 (vous)")
            if 0 in losers:
                losers.remove(0)
                losers.append("0 (vous)")

            # Prépare et affiche les gagnants / perdants.
            winner_str = "".join(
                [f"Joueur {y} " if len(winners) == 1 or x + 1 == len(winners) else f"Joueur {y} et " if 1 < len(
                    winners) != x + 1 else print() for x, y in enumerate(winners)])
            display.screen.blit(display.ultra_small_font.render(winner_str, False, (255, 255, 255)),
                                (display.w / 2.6, display.h / 2.6))

            losers_str = textwrap.fill("".join([f"Joueur {y} " if len(losers) == 1 or x + 1 == len(
                losers) else f"Joueur {y} et " if 1 < len(losers) != x + 1 else "" for x, y in enumerate(losers)]),
                                       35)
            losers_str = losers_str.split("\n")

            for y, text in enumerate(sorted(losers_str, reverse=True)):
                display.screen.blit(display.ultra_small_font.render(text, 35, False, (255, 255, 255)),
                                    (display.w / 2.6, display.h / 2.05 - y * 20))

            button_rematch.update(display.screen)

        else:
            #  Tour suivant
            button_ok.update(display.screen)
            if ok:
                game.next_round(as_func, retire_func)
                ok = False

        # Actualise l'interface
        display.update()

        for event in display.pg_events:
            # Vérifie si boutons cliques (la fonction dans le module ne convient pas à ce que je veux faire.)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_ok.rect.collidepoint(event.pos):
                    ok = True
                if button_rematch.rect.collidepoint(event.pos) and (game.cards_remaining == 0 or game.j_cards == {}):
                    game.reset_cards()
                    ok = True
                    reveal = False
