import random
import typing


class BlackJackGame:
    def __init__(self, nbr_jrs: int = 2):
        self.j_perm_cards = {}
        self.cards_remaining = 0
        self.tour = 1
        self.nbr_jrs = nbr_jrs
        self.j_cards = self.cartes_dispos = self.players_result = None

        self.default_cards = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Valet", "Dame", "Roi"]

        self.reset_cards()  # Crée la partie

    def reset_cards(self):
        """
        Réinitialise la partie et remet tous les compteurs à 0.
        """
        self.tour = 1
        self.j_cards = {}
        self.j_perm_cards = {}
        self.players_result = {}
        self.cartes_dispos = {"Piques": self.default_cards[0:len(self.default_cards)], "Carreaux": self.default_cards[0:len(self.default_cards)],
                              "Coeurs": self.default_cards[0:len(self.default_cards)], "Trèfles": self.default_cards[0:len(self.default_cards)]}
        for jrs in range(self.nbr_jrs):
            self.players_result[jrs] = 0
            self.j_cards[jrs] = []
            self.j_perm_cards[jrs] = []
        self.cards_remaining = 0
        for cards in self.cartes_dispos:
            self.cards_remaining += len(self.cartes_dispos[cards])

    def next_round(self, as_function: typing.Callable, retire_function: typing.Callable):
        """
        :param as_function: Créer une fonction dans le cas où le joueur doit effectuer un choix quant à un AS. Doit prendre un argument 'joueur' pour savoir quel est le joueur concerné.
        :param retire_function: Créer une fonction dans le cas où le joueur doit effectuer un choix s'il veut se retirer de la partie (après avoir un score supérieur ou égale à 16). Doit prendre un argument 'joueur' pour savoir quel est le joueur concerné.
        Passer au prochain tour.\n
        Ne retourne rien.
        """
        self.tour += 1
        for jrs in list(self.j_cards.keys()):

            for exp in list(self.cartes_dispos):  # Vérifie s'il y a toujours des cartes dans le paquet.
                if self.cartes_dispos[exp] == []:
                    self.cartes_dispos.pop(exp)
            if self.cartes_dispos == {}:
                # print('Plus de cartes dans le paquet')
                self.j_cards.clear()
                return "Cards limit reach"

            exp = random.choice(list(self.cartes_dispos.keys()))  # Donne une carte au joueur
            card = random.choice(self.cartes_dispos[exp])

            self.j_cards[jrs].append({exp: card})
            self.j_perm_cards[jrs].append({exp: card})
            self.cartes_dispos[exp].remove(card)
            if jrs == 0:
                pass
                # print(f"Joueur {jrs} a récupéré un {card} de {exp}.")
            else:
                pass
                # print(f"Joueur {jrs} a récupéré une carte.")
            if len(card) <= 2 and card != "As":  # Ajoute le score des cartes
                self.players_result[jrs] += int(card)
            elif len(card) >= 3:
                self.players_result[jrs] += 10
            elif card == "As":
                as_response = 0
                while as_response not in [1, 11]:
                    as_response = as_function(jrs)
                self.players_result[jrs] += as_response

            if jrs == 0:
                pass
                # print(f"Joueur {jrs} avez {self.j_cards[jrs]}")

        for player in list(self.j_cards.keys()):  # Vérifie si un joueur est éliminé / s'il veut se retirer.
            if self.players_result[player] > 21:
                self.j_cards.pop(player)
            elif self.players_result[player] >= 16:
                response = None
                while response not in [True, False]:
                    response = retire_function(player)
                if response is True:
                    self.j_cards.pop(player)

        self.cards_remaining = 0
        for cards in self.cartes_dispos:
            self.cards_remaining += len(self.cartes_dispos[cards])
        # print(f"Tour {self.tour}")

    def get_score(self):
        """
        :return: winners, looser

        Winners sont les gagnants du jeu.\n
        Looser sont les perdants du jeu.\n

        Il peut y avoir plusieurs gagnants dans le cas d'une égalité.
        """
        winners = []
        looser = []
        # print(self.players_result)
        for player in self.players_result:  # Change les joueurs au score supérieur à 21.
            if self.players_result[player] > 21:
                self.players_result[player] = 0

        for player in list(self.players_result.keys()):  # Trouve les gagnants / Perdants
            if self.players_result[player] == max(list(self.players_result.values())) and \
                    self.players_result[player] <= 21:
                winners.append(player)
            else:
                looser.append(player)
        return winners, looser


if "__main__" == __name__:
    """
    LANCER LE JEU
    """

    game = BlackJackGame(int(input("Combien de joueurs?: ")))
    print("Vous êtes joueur 0.")


    def as_test(joueur):
        if joueur == 0:
            while True:
                choice = input("Voulez vous l'utiliser comme 1 ou 11?: ")
                if choice.isnumeric() and (int(choice) == 1 or int(choice) == 11):
                    return int(choice)
        else:
            if game.players_result[joueur] >= 10:
                return 11
            else:
                return 1


    def stop_test(joueur):
        if joueur == 0:
            while True:
                choice = str.upper(input("Voulez vous vous arrêter?(O/N): "))
                if choice == "O" or choice == "N":
                    if choice == "O":
                        return True
                    else:
                        return False
        else:
            if game.players_result[joueur] > 17:
                return False
            else:
                # print(f"{joueur} s'est arrêté.")
                return True


    while game.cards_remaining > 0:
        game.next_round(as_test, stop_test)
    print(f"Gagnants: joueur {game.get_score()[0]}, perdants: joueurs {game.get_score()[1]}")
