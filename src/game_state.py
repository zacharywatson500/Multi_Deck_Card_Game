"""Game state and controller classes for managing the central game logic."""

from typing import Dict, Any
from deck import Deck
from player import Player


class GameState:
    """
    Pure data container (the "Model") for the game state.
    
    Attributes:
        decks (Dict[str, Deck]): Dictionary of Deck instances.
        player (Player): The Player instance.
        turn_number (int): Current turn number.
        energy (int): Available energy for the current turn.
        is_game_over (bool): Game over status.
    """
    
    def __init__(self, decks: Dict[str, Deck], player: Player) -> None:
        """
        Initialize a GameState instance.
        
        Args:
            decks (Dict[str, Deck]): Dictionary of Deck instances (e.g., {"Main": deck_obj, "Resource": res_obj}).
            player (Player): The Player instance.
        """
        self.decks = decks
        self.player = player
        self.turn_number = 1
        self.energy = 0
        self.is_game_over = False
    
    def __repr__(self) -> str:
        """
        Return string representation of the game state.
        
        Returns:
            str: Information about current game state.
        """
        return f"GameState(Turn: {self.turn_number}, Energy: {self.energy}, Game Over: {self.is_game_over})"


class GameController:
    """
    Handles the game logic (the "Referee").
    
    The Controller is the only thing that should modify the data inside the State.
    
    Attributes:
        state (GameState): Reference to the GameState instance.
    """
    
    def __init__(self, state: GameState) -> None:
        """
        Initialize a GameController instance.
        
        Args:
            state (GameState): The GameState instance to manage.
        """
        self.state = state
    
    def start_turn(self) -> None:
        """
        Start a new turn by incrementing turn number, resetting energy, and drawing cards.
        
        This method:
        1. Increments self.state.turn_number
        2. Resets self.state.energy to 3
        3. Draws 1 card from "Main" deck and 1 card from "Resource" deck
        """
        # Increment turn number
        self.state.turn_number += 1
        
        # Reset energy to default of 3
        self.state.energy = 3
        
        # Draw 1 card from Main deck
        if "Main" in self.state.decks:
            self.state.player.draw_from(self.state.decks["Main"], 1)
        
        # Draw 1 card from Resource deck
        if "Resource" in self.state.decks:
            self.state.player.draw_from(self.state.decks["Resource"], 1)
    
    def __repr__(self) -> str:
        """
        Return string representation of the game controller.
        
        Returns:
            str: Information about the controller and its state.
        """
        return f"GameController({self.state})"


if __name__ == "__main__":
    # Example usage
    from card import Card
    
    # Create test cards for decks
    main_cards = [
        Card("Fireball", "Main", 3, "Deal 3 damage"),
        Card("Heal", "Main", 2, "Restore 2 health"),
        Card("Lightning", "Main", 4, "Deal 4 damage")
    ]
    
    resource_cards = [
        Card("Energy Crystal", "Resource", 1, "Gain 1 energy"),
        Card("Mana Potion", "Resource", 2, "Gain 2 energy"),
        Card("Power Gem", "Resource", 3, "Gain 3 energy")
    ]
    
    # Create decks
    main_deck = Deck(main_cards)
    resource_deck = Deck(resource_cards)
    
    # Create player
    player = Player("Test Player")
    
    # Create game state
    decks = {"Main": main_deck, "Resource": resource_deck}
    game_state = GameState(decks, player)
    
    # Create controller
    controller = GameController(game_state)
    
    print(f"Initial state: {game_state}")
    print(f"Initial player: {player}")
    
    # Start first turn
    print("\n--- Starting Turn 1 ---")
    controller.start_turn()
    print(f"State after turn 1: {game_state}")
    print(f"Player after turn 1: {player}")
    
    # Start second turn
    print("\n--- Starting Turn 2 ---")
    controller.start_turn()
    print(f"State after turn 2: {game_state}")
    print(f"Player after turn 2: {player}")
