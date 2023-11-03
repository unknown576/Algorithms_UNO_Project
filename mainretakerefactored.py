import random


class UNOGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.colors = ["Red", "Green", "Yellow", "Blue"]
        self.numbers = [str(i) for i in range(10)]
        self.specials = ["Draw Two", "Skip", "Reverse"]
        self.wilds = ["Wild Card", "Wild Draw Four"]
        self.players = [[] for _ in range(num_players)]
        self.current_player = 0
        self.direction = 1
        self.game_deck, self.top_card, self.split_card = self.build_and_shuffle_deck()
        self.discards = [self.top_card]
        self.current_color, self.card_value = self.split_card

    def build_and_shuffle_deck(self):
        game_deck = []

        for color in self.colors:
            for number in self.numbers:
                for _ in range(2):
                    if number == "0":
                        card = f"{color} {number}"
                    else:
                        card = f"{color} {number}"
                    game_deck.append(card)

            for special in self.specials:
                card = f"{color} {special}"
                game_deck.extend([card] * 2)

        for _ in range(4):
            game_deck.extend(self.wilds)

        random.shuffle(game_deck)
        top_card = game_deck.pop(0)

        while top_card.startswith("Wild") or top_card.split()[1] in self.specials:
            random.shuffle(game_deck)
            top_card = game_deck.pop(0)

        split_card = top_card.split()
        return game_deck, top_card, split_card

    def draw_cards(self, num_cards):
        drawn_cards = []
        for _ in range(num_cards):
            drawn_cards.append(self.game_deck.pop(0))
        return drawn_cards

    def valid_card(self, color, value, player_hand):
        for card in player_hand:
            card_parts = card.split()
            if "Wild" in card or (len(card_parts) == 2 and (color == card_parts[0] or value == card_parts[1])):
                return True
        return False

    def current_hand(self):

        # See why players hands are all blank at start, should be filled dto 7 cards each

        print(f"Player {self.current_player + 1} is now playing.")
        print("Your Current Hand:")
        print("......................")
        for i, card in enumerate(self.players[self.current_player], start=1):
            print(card)
        print(" ")

    def start_game(self):
        while self.num_players < 2 or self.num_players > 4:
            try:
                self.num_players = int(input("How Many People are playing: "))
                if not (2 <= self.num_players <= 4):
                    print("ERROR: Number of players invalid, please give a value of 2, up to 4.")
            except ValueError:
                print("ERROR: Please enter a valid integer.")

        self.number_of_players()

    def number_of_players(self):
        for player in range(self.num_players):
            self.players[player] = self.draw_cards(7)

    def play_turn(self):
        self.current_hand()
        print("Top of pile:", self.discards[-1])

        if self.valid_card(self.current_color, self.card_value, self.players[self.current_player]):
            chosen_card = int(input("Please select a card to play: ")) - 1

            while not (0 <= chosen_card < len(self.players[self.current_player])) or not self.valid_card(
                    self.current_color, self.card_value, [self.players[self.current_player][chosen_card]]):
                chosen_card = int(input("Please choose a valid card to play: ")) - 1

            print("You have played", self.players[self.current_player][chosen_card])
            self.discards.append(self.players[self.current_player].pop(chosen_card))
        else:
            print(f"Player {self.current_player + 1} No cards available are valid to play, please pick up from the pile.")
            self.players[self.current_player].extend(self.draw_cards(1))

        split_card = self.discards[-1].split()
        self.current_color, self.card_value = split_card

        if self.current_color == "Wild":
            for i, color in enumerate(self.colors, start=1):
                print(f"{i} {color}")
            color_update = int(input("What color would you like to change to: ")) - 1

            while color_update < 0 or color_update >= len(self.colors):
                color_update = int(input("Invalid Option Given. What color would you like to change to: ")) - 1

            self.current_color = self.colors[color_update]
            print("Colour has been changed to:", self.current_color)

            if self.card_value == "Draw Four":
                next_player = (self.current_player + self.direction) % self.num_players
                print(f"Player {next_player + 1} is drawing 4 more cards.")
                self.players[next_player].extend(self.draw_cards(4))

        if self.card_value == "Reverse":
            print("Direction of play has been reversed.")
            self.direction *= -1

        if self.card_value == "Skip":
            print("Next Player has been skipped.")
            self.current_player = (self.current_player + self.direction) % self.num_players

        if self.card_value == "Draw Two":
            next_player = (self.current_player + self.direction) % self.num_players
            print(f"Player {next_player + 1} is drawing 2 more cards.")
            self.players[next_player].extend(self.draw_cards(2))

        self.current_player = (self.current_player + self.direction) % self.num_players

        if self.current_player < 0:
            self.current_player = self.num_players - 1

    def play_game(self):
        while True:
            self.play_turn()


if __name__ == "__main__":
    num_players = None
    while num_players is None:
        try:
            num_players = int(input("How Many People are playing: "))
            if not (2 <= num_players <= 4):
                print("ERROR: Number of players invalid, please give a value of 2, up until 4.")
                num_players = None
        except ValueError:
            print("ERROR: Please enter a valid integer.")

    uno_game = UNOGame(num_players)
    uno_game.play_game()