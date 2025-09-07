"""
File: py_uno.py
Author: Bliss Phinehas
Date: 2024-04-22
Description: This program implements a simplified version of the UNO game.
"""

import random

# Constants for card attributes
COLORS = ['Red', 'Green', 'Blue', 'Yellow']
CARD_COLOR = 'color'
CARD_NUMBER = 'number'
CARD_SPECIAL = 'special'
SKIP = 'Skip'
DRAW_TWO = 'DrawTwo'
WILD = 'Wild'
WILD_DRAW_FOUR = 'WildDrawFour'
COLOR_SPECIALS = [SKIP, DRAW_TWO]
WILD_SPECIALS = [WILD, WILD_DRAW_FOUR]
NUM_STARTING_CARDS = 7  # Number of cards each player starts with


def create_deck():
    """
    Creates a standard UNO deck with specified modifications.

    :return: A list representing the deck of cards.
    """

    deck = [
        {CARD_COLOR: the_color,
         CARD_NUMBER: i % 10,
         CARD_SPECIAL: ''
         }
        for i in range(20)
        for the_color in COLORS
    ]

    for special in COLOR_SPECIALS:
        for the_color in COLORS:
            special_card = {
                CARD_COLOR: the_color,
                CARD_NUMBER: -1,
                CARD_SPECIAL: special
            }
            deck.append(dict(special_card))
            deck.append(dict(special_card))

    for special in WILD_SPECIALS:
        special_card = {
            CARD_COLOR: '',
            CARD_NUMBER: -1,
            CARD_SPECIAL: special
        }
        for i in range(4):
            deck.append(dict(special_card))

    return deck


def deal_cards(deck, num_players=2, cards_per_player=NUM_STARTING_CARDS):
    """
    Deals cards to players from the deck in alternating fashion.

    :param deck: The deck of cards (list of dictionaries).
    :param num_players: The number of players (default is 2).
    :param cards_per_player: Number of cards to deal to each player (default is 7).
    :return: A tuple containing the updated deck and a list of player hands.
    """

    player_hands = [[] for _ in range(num_players)]

    for _ in range(cards_per_player):
        for player_index in range(num_players):
            if deck:  # Check if deck still has cards
                player_hands[player_index].append(deck.pop(0))

    return deck, player_hands


def card_to_string(card):
    """
    Converts a card dictionary to a string representation.

    :param card: The card (dictionary).
    :return: The string representation of the card.
    """

    if card[CARD_SPECIAL]:
        if card[CARD_COLOR]:  # For colored special cards
            return f"{card[CARD_COLOR]}{card[CARD_SPECIAL]}"
        else:  # For wild cards without a chosen color
            return f"{card[CARD_SPECIAL]}"
    else:
        return f"{card[CARD_COLOR]}{card[CARD_NUMBER]}"


def display_hand(hand):
    """
    Displays a player's hand in a readable format.

    :param hand: A list of card dictionaries representing the player's hand.
    :return: None
    """

    card_strings = [card_to_string(card) for card in hand]
    print(' '.join(card_strings))


def is_valid_play(card, top_card, current_color):
    """
    Checks if a card can be played on top of the current top card.

    :param card: The card being played (dictionary).
    :param top_card: The current top card on the discard pile (dictionary).
    :param current_color: The current active color.
    :return: True if the card is a valid play, False otherwise.
    """

    # Wild cards can be played anytime
    if card[CARD_SPECIAL] in WILD_SPECIALS:
        return True

    # Match by color
    if card[CARD_COLOR] == current_color:
        return True

    # Match by number (if not a special card)
    if card[CARD_NUMBER] == top_card[CARD_NUMBER] and card[CARD_NUMBER] != -1:
        return True

    # Match by special type (for Skip and DrawTwo)
    if card[CARD_SPECIAL] and card[CARD_SPECIAL] == top_card[CARD_SPECIAL]:
        return True

    return False


def find_card_in_hand(hand, card_name):
    """
    Finds a card in the hand by its string representation.

    :param hand: The player's hand (list of dictionaries).
    :param card_name: The string representation of the card.
    :return: The index of the card in the hand, or None if not found.
    """

    # Check each card in the hand
    for i, card in enumerate(hand):
        if card_to_string(card) == card_name:
            return i

    # Card not found
    return None


def handle_special_card(card, discard_pile, deck, player_hands, current_player):
    """
    Handles the effects of special cards (Skip, DrawTwo, Wild, WildDrawFour).

    :param card: The special card played (dictionary).
    :param discard_pile: The discard pile.
    :param deck: The game deck (list of dictionaries).
    :param player_hands: List of player hands (list of lists of dictionaries).
    :param current_player: The index of the current player.
    :return: The index of the next player, considering skips and draw penalties.
             Returns -1 if the game ends due to an empty draw pile.
    """

    next_player = (current_player + 1) % len(player_hands)

    if card[CARD_SPECIAL] == SKIP:
        # Skip the next player's turn
        return (current_player + 2) % len(player_hands)

    elif card[CARD_SPECIAL] == DRAW_TWO:
        # Next player draws two cards and skips their turn
        for _ in range(2):
            if deck:
                player_hands[next_player].append(deck.pop(0))
            else:
                return -1  # Game ends in a tie
        return (current_player + 2) % len(player_hands)

    elif card[CARD_SPECIAL] == WILD_DRAW_FOUR:
        # Next player draws four cards and skips their turn
        for _ in range(4):
            if deck:
                player_hands[next_player].append(deck.pop(0))
            else:
                return -1  # Game ends in a tie
        return (current_player + 2) % len(player_hands)

    elif card[CARD_SPECIAL] == WILD:
        # Wild card doesn't skip turns
        return next_player

    # For normal cards
    return next_player


def select_valid_color():
    """
    Prompts the user to select a valid color.

    :return: A valid color selected by the user.
    """
    valid_color = False
    color_choice = ""

    while not valid_color:
        color_choice = input("Select a color [Blue, Red, Green, Yellow] ")
        if color_choice in COLORS:
            valid_color = True
        else:
            # Keep prompting until valid color selected
            pass

    return color_choice


def play_uno():
    """
    Main function to run the PyUNO game.

    :return: None
    """

    # Initialize the game
    the_deck = create_deck()
    the_seed = input('What seed do you want to use for the game? ')
    random.seed(the_seed)
    random.shuffle(the_deck)

    # Deal cards to players
    the_deck, player_hands = deal_cards(the_deck)

    # Initialize game state
    discard_pile = []
    current_color = ""

    # Print initial game state before any cards are played
    print("__")
    display_hand(player_hands[0])

    # Game variables
    current_player = 0
    has_drawn = False
    game_over = False

    # Main game loop
    while not game_over:
        # Get player action
        player_prompt = f"Player {current_player + 1}, what would you like to do? "
        user_input = input(player_prompt)
        action_parts = user_input.split(' ', 1)

        # Process user action
        valid_action = False

        if len(action_parts) > 0:
            action = action_parts[0].lower()

            # Handle play action
            if action == 'play' and len(action_parts) > 1:
                card_name = action_parts[1]
                card_index = find_card_in_hand(player_hands[current_player], card_name)

                # Check if card exists in hand
                if card_index is not None:
                    card = player_hands[current_player][card_index]

                    # Handle first play of the game
                    if not discard_pile:
                        # First card can be anything
                        played_card = player_hands[current_player].pop(card_index)
                        discard_pile.append(played_card)

                        # Set current color based on played card
                        if played_card[CARD_SPECIAL] in WILD_SPECIALS:
                            color_choice = select_valid_color()
                            current_color = color_choice
                            played_card[CARD_COLOR] = color_choice
                        else:
                            current_color = played_card[CARD_COLOR]

                        valid_action = True
                    else:
                        # Check if card can be played on top of current card
                        if is_valid_play(card, discard_pile[-1], current_color):
                            played_card = player_hands[current_player].pop(card_index)
                            discard_pile.append(played_card)

                            # Handle Wild card color selection
                            if played_card[CARD_SPECIAL] in WILD_SPECIALS:
                                color_choice = select_valid_color()
                                current_color = color_choice
                                played_card[CARD_COLOR] = color_choice
                            else:
                                current_color = played_card[CARD_COLOR]

                            valid_action = True
                        else:
                            print("That card didn't match in number or color.")
                else:
                    print("That card is not in your hand.")

            # Handle draw action
            elif action == 'draw':
                if not has_drawn:
                    if the_deck:
                        # Draw a card from the deck
                        player_hands[current_player].append(the_deck.pop(0))
                        has_drawn = True
                        display_hand(player_hands[current_player])
                        valid_action = True
                    else:
                        print("Draw pile is empty! Game ends in a tie.")
                        game_over = True
                else:
                    print("You can only draw once per turn.")

            # Handle pass action
            elif action == 'pass':
                if has_drawn:
                    # Valid pass action
                    valid_action = True
                else:
                    print("You must draw a card before passing.")
            else:
                print("Invalid action. Use 'play [CardName]', 'draw', or 'pass'.")

        # Process outcome of valid action
        if valid_action:
            if action == 'play':
                # Display the top card after a play
                print(f"The top card is:  {card_to_string(discard_pile[-1])}")

                # Check for win
                if len(player_hands[current_player]) == 0:
                    print(f"Congratulations Player {current_player + 1}! You Won!")
                    game_over = True
                else:
                    # Determine next player based on special card effects
                    if played_card[CARD_SPECIAL]:
                        next_player = handle_special_card(played_card, discard_pile, the_deck,
                                                         player_hands, current_player)
                        if next_player == -1:
                            print("Draw pile is empty! Game ends in a tie.")
                            game_over = True
                        else:
                            current_player = next_player
                    else:
                        current_player = (current_player + 1) % len(player_hands)

                    # Reset has_drawn for new turn
                    has_drawn = False

                    # Display next player's hand if game continues
                    if not game_over:
                        display_hand(player_hands[current_player])

            elif action == 'pass':
                # Move to next player
                current_player = (current_player + 1) % len(player_hands)
                has_drawn = False

                if discard_pile:
                    print(f"The top card is:  {card_to_string(discard_pile[-1])}")

                # Display next player's hand
                display_hand(player_hands[current_player])


if __name__ == '__main__':
    play_uno()