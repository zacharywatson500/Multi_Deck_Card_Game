"""Game state and controller classes for managing the central game logic."""

from typing import Dict, Any, List
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
        self.message_log: List[str] = ["Welcome to the Three-Deck System!"]
    
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
    
    def log_event(self, message: str) -> None:
        """
        Log an event to the message log, keeping only the last 50 messages.
        
        Args:
            message (str): The message to log.
        """
        self.state.message_log.append(message)
        # Keep only the last 50 messages
        if len(self.state.message_log) > 50:
            self.state.message_log = self.state.message_log[-50:]
    
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
        
        # Log turn start
        self.log_event(f"--- Turn {self.state.turn_number} Started ---")
        
        # Reset energy to default of 3
        self.state.energy = 3
        
        # Draw 1 card from Main deck
        if "Main" in self.state.decks:
            self.state.player.draw_from(self.state.decks["Main"], 1)
        
        # Draw 1 card from Resource deck
        if "Resource" in self.state.decks:
            self.state.player.draw_from(self.state.decks["Resource"], 1)
    
    def resolve_enemy_turn(self):
        """
        Resolve the enemy turn by drawing an encounter card and dealing damage.
        
        This method:
        1. Draws 1 card from "Encounter" deck
        2. Subtracts the card's current_value from player.life_total
        3. Moves the drawn card to the Encounter deck's discard pile
        4. Returns the drawn Card object
        
        Returns:
            Card or None: The drawn encounter card, or None if no cards available
        """
        # Check if Encounter deck exists and has cards
        if "Encounter" not in self.state.decks:
            return None
        
        encounter_deck = self.state.decks["Encounter"]
        
        # Draw 1 card from Encounter deck
        drawn_cards = encounter_deck.draw(1)
        
        if not drawn_cards:
            return None
        
        enemy_card = drawn_cards[0]
        
        # Log enemy attack
        self.log_event(f"The {enemy_card.name} attacks for {enemy_card.current_value} damage!")
        
        # Subtract damage from player life total
        self.state.player.life_total -= enemy_card.current_value
        
        # Move card to discard pile
        encounter_deck.add_to_discard(enemy_card)
        
        return enemy_card
    
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
