"""Game factory module for setting up the Four-Deck card game."""

from typing import Tuple, List

from .card import Card
from .deck import Deck
from .player import Player
from .game_state import GameState, GameController
from .database_manager import initialize_database, get_random_cards


def setup_game() -> Tuple[GameState, GameController]:
    """
    Card Factory helper function that sets up the game using database-loaded cards.
    
    Returns:
        Tuple[GameState, GameController]: The initialized game state and controller.
    """
    # Initialize the database (creates it if it doesn't exist)
    initialize_database()
    
    # Instantiate a Player
    player = Player("Hero", life_total=20, resource_level=0)
    
    # Get 5 random cards from each deck type for starting decks
    attack_card_data = get_random_cards("Attack", 5)
    healing_card_data = get_random_cards("Healing", 5)
    resource_card_data = get_random_cards("Resource", 5)
    encounter_card_data = get_random_cards("Encounter", 5)
    
    # Fail-fast: Check if database has enough cards
    if not attack_card_data or not healing_card_data or not resource_card_data or not encounter_card_data:
        raise RuntimeError("Database doesn't have enough cards. Please run 'python seed_db.py' to initialize card data.")
    
    # Convert card data tuples to Card objects
    attack_cards = [Card(name, deck_type, value, category, description) 
                   for name, deck_type, value, category, description in attack_card_data]
    healing_cards = [Card(name, deck_type, value, category, description) 
                    for name, deck_type, value, category, description in healing_card_data]
    resource_cards = [Card(name, deck_type, value, category, description) 
                      for name, deck_type, value, category, description in resource_card_data]
    encounter_cards = [Card(name, deck_type, value, category, description) 
                       for name, deck_type, value, category, description in encounter_card_data]
    
    # Create four Deck instances using these cards
    attack_deck = Deck(attack_cards)
    healing_deck = Deck(healing_cards)
    resource_deck = Deck(resource_cards)
    encounter_deck = Deck(encounter_cards)
    
    # Shuffle all decks
    attack_deck.shuffle()
    healing_deck.shuffle()
    resource_deck.shuffle()
    encounter_deck.shuffle()
    
    # Initialize a GameState with the decks and player
    decks = {
        "Attack": attack_deck,
        "Healing": healing_deck,
        "Resource": resource_deck,
        "Encounter": encounter_deck
    }
    game_state = GameState(decks, player)
    
    # Create a GameController with that state
    game_controller = GameController(game_state)
    
    # Initialize Turn 1
    game_controller.start_turn()
    
    return game_state, game_controller
