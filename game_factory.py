"""Game factory module for setting up the Tri-Deck card game."""

from typing import Tuple

from card import Card
from deck import Deck
from player import Player
from game_state import GameState, GameController


def setup_game() -> Tuple[GameState, GameController]:
    """
    Dummy Card Factory helper function that sets up the game.
    
    Returns:
        Tuple[GameState, GameController]: The initialized game state and controller.
    """
    # Instantiate a Player
    player = Player("Hero", life_total=20, resource_level=0)
    
    # Generate three distinct lists of Card objects
    # Attack cards for "Main" deck
    main_cards = [
        Card("Fireball", "Main", 3, "Attack", "Deal 3 damage to enemy"),
        Card("Sword Strike", "Main", 2, "Attack", "Deal 2 damage to enemy"),
        Card("Lightning Bolt", "Main", 4, "Attack", "Deal 4 damage to enemy"),
        Card("Ice Shard", "Main", 2, "Attack", "Deal 2 damage to enemy"),
        Card("Arrow Shot", "Main", 1, "Attack", "Deal 1 damage to enemy"),
        Card("Healing Potion", "Main", 3, "Healing", "Restore 3 health"),
        Card("Regeneration", "Main", 2, "Healing", "Restore 2 health")
    ]
    
    # Energy cards for "Resource" deck
    resource_cards = [
        Card("Energy Crystal", "Resource", 1, "Resource", "Gain 1 energy"),
        Card("Mana Potion", "Resource", 2, "Resource", "Gain 2 energy"),
        Card("Power Gem", "Resource", 3, "Resource", "Gain 3 energy"),
        Card("Focus Charm", "Resource", 1, "Resource", "Gain 1 energy"),
        Card("Meditation", "Resource", 2, "Resource", "Gain 2 energy")
    ]
    
    # Enemy cards for "Encounter" deck
    enemy_cards = [
        Card("Goblin", "Encounter", 2, "Attack", "Enemy with 2 health"),
        Card("Orc", "Encounter", 4, "Attack", "Enemy with 4 health"),
        Card("Dragon", "Encounter", 8, "Attack", "Enemy with 8 health"),
        Card("Skeleton", "Encounter", 1, "Attack", "Enemy with 1 health"),
        Card("Troll", "Encounter", 6, "Attack", "Enemy with 6 health")
    ]
    
    # Create three Deck instances using these cards
    main_deck = Deck(main_cards)
    resource_deck = Deck(resource_cards)
    encounter_deck = Deck(enemy_cards)
    
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
