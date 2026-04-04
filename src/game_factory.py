"""Game factory module for setting up the Tri-Deck card game."""

from typing import Tuple, List

from .card import Card
from .deck import Deck
from .player import Player
from .game_state import GameState, GameController
from .database_manager import initialize_database, get_all_cards


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
    
    # Load all cards from the database
    card_data = get_all_cards()
    
    # Fail-fast: Check if database is empty
    if not card_data:
        raise RuntimeError("Database is empty. Please run 'python seed_db.py' to initialize card data.")
    
    # Separate cards by deck type
    main_cards = []
    resource_cards = []
    encounter_cards = []
    
    for name, deck_type, value, category, description in card_data:
        card = Card(name, deck_type, value, category, description)
        
        if deck_type == "Main":
            main_cards.append(card)
        elif deck_type == "Resource":
            resource_cards.append(card)
        elif deck_type == "Encounter":
            encounter_cards.append(card)
    
    # Create three Deck instances using these cards
    main_deck = Deck(main_cards)
    resource_deck = Deck(resource_cards)
    encounter_deck = Deck(encounter_cards)
    
    # Shuffle all decks
    main_deck.shuffle()
    resource_deck.shuffle()
    encounter_deck.shuffle()
    
    # Initialize a GameState with the decks and player
    decks = {
        "Main": main_deck,
        "Resource": resource_deck,
        "Encounter": encounter_deck
    }
    game_state = GameState(decks, player)
    
    # Create a GameController with that state
    game_controller = GameController(game_state)
    
    # Initialize Turn 1
    game_controller.start_turn()
    
    return game_state, game_controller
