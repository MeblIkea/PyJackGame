import sys
import os
import math
import pygame
from pygame.locals import *


class Cartes:
    def __init__(self):
        """
        Initialise l'objet Cartes.
        """
        self.cards = {"Reversed": [pygame.transform.smoothscale(pygame.image.load(r"cartes\Reversed.png"), (112, 163)),
                                   pygame.image.load(r"cartes\Reversed.png")]}
        for card_dir in (x for x in os.listdir("cartes") if (x != "Reversed.png" and x != "icon.ico")):
            self.cards[card_dir] = {}
            for card in os.listdir(rf"cartes/{card_dir}"):
                self.cards[card_dir][card.split(".")[0]] = pygame.transform.smoothscale(
                    pygame.image.load(rf"cartes\{card_dir}\{card}"), (112, 163))

    @staticmethod
    def trigo_calc(rad: int or float, multi: int = 100, centre: (int, int) = (0, 0)):
        """
        :param rad: Donner la valeur avec pi.
        :param multi: Éloigne le point du centre (avant arrondir).
        :param centre: Point du centre (pour centrer).
        :return: Position X et Y du point.
        Calcule la position de la carte.
        """
        return round(math.cos(rad) * multi + centre[0]), round(math.sin(rad) * multi + centre[1])


class Display:
    def __init__(self):
        """
        Initialise l'objet Display.
        """
        pygame.init()
        self.pg_events = []
        self.screen = pygame.display.set_mode((960, 810))
        self.clock = pygame.time.Clock()
        self.h, self.w = self.screen.get_size()

        self.ultra_small_font = pygame.font.SysFont("Arial", 20)
        self.small_font = pygame.font.SysFont("Arial Bold", 40)
        self.default_font = pygame.font.SysFont("Arial Bold", 55)
        self.huge_font = pygame.font.SysFont("Arial Bold", 100)

        self.error = ""  # Pour afficher une erreur

        pygame.display.set_caption("PyJackGame")
        pygame.display.set_icon(pygame.image.load(r"cartes/icon.ico"))

    def reset_error(self):
        """
        Reinitialise la valeur self.error.
        """
        self.error = ""

    def board(self):
        """
        Met le fond en mode plateau de jeu.
        """
        self.screen.fill((0, 110, 0), (0, 0, self.h, self.w))
        self.screen.blit(self.ultra_small_font.render("Pressez Echap pour quitter", True, (0, 100, 0)), (0, 0))

    def update(self):
        """
        Actualise tout l'écran.
        """
        self.clock.tick(30)

        error_text = self.small_font.render(self.error, False, (170, 0, 0))
        self.screen.blit(error_text, (error_text.get_rect(center=(self.h / 2, 0))[0], self.w / 1.4))
        pygame.display.flip()

        self.pg_events = pygame.event.get()
        for event in self.pg_events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == pygame.K_ESCAPE):  # Quit
                sys.exit()
