"""Game state and controller classes for managing the central game logic."""

from typing import Dict, Any, List
from .deck import Deck
from .player import Player
from .card import Card
from .database_manager import get_card_by_name


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
        self.turn_number = 0
        self.energy = 0
        self.is_game_over = False
        self.current_enemy_health = 10
        self.message_log: List[str] = ["Welcome to the Three-Deck System!"]
        self.player_deck: List[Card] = []  # Player's personal deck for deck-building
    
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
        Start a new turn by incrementing turn number and resetting energy to 5.
        
        This method:
        1. Increments self.state.turn_number
        2. Resets self.state.energy to 5
        """
        # Increment turn number
        self.state.turn_number += 1
        
        # Log turn start
        self.log_event(f"--- Turn {self.state.turn_number} Started ---")
        
        # Reset energy to 5
        self.state.energy = 5
    
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
    
    def can_play_card(self, index: int) -> bool:
        """
        Check if a card can be played from the player's hand.
        
        Args:
            index (int): Index of the card in the player's hand.
            
        Returns:
            bool: True if the card can be played, False otherwise.
        """
        # Check if the card index is valid for the hand
        if index < 0 or index >= len(self.state.player.hand):
            return False
        
        card = self.state.player.hand[index]
        
        # If the card is a "Resource" category, return True (bypasses energy checks)
        if card.category == "Resource":
            return True
        
        # If not a Resource, return True only if self.state.energy >= card.current_value
        return self.state.energy >= card.current_value
    
    def resolve_card(self, index: int) -> bool:
        """
        Resolve playing a card from the player's hand.
        
        Args:
            index (int): Index of the card in the player's hand.
            
        Returns:
            bool: True if the card was successfully played, False otherwise.
        """
        # Retrieve the card and its target_deck_type
        if index < 0 or index >= len(self.state.player.hand):
            return False
        
        card = self.state.player.hand[index]
        target_deck_type = card.deck_type
        
        # Call self.state.player.play_card(index, self.state.decks[target_deck_type])
        played_card = self.state.player.play_card(index, self.state.decks[target_deck_type])
        
        if not played_card:
            return False
        
        # Logic Branching
        if played_card.category == "Resource":
            # Add current_value to self.state.energy and log "✨ Gained [X] energy from [Name]"
            self.state.energy += played_card.current_value
            self.log_event(f"✨ Gained {played_card.current_value} energy from {played_card.name}")
        elif played_card.category == "Healing":
            # Increase player life_total and log healing
            self.state.player.life_total += played_card.current_value
            self.state.energy -= played_card.current_value
            self.log_event(f"💚 Healed {played_card.current_value} health from {played_card.name}")
        else:  # Attack category
            # Subtract current_value from self.state.energy and log attack
            self.state.energy -= played_card.current_value
            
            # Reduce enemy health
            self.state.current_enemy_health -= played_card.current_value
            
            # Check if enemy is defeated
            if self.state.current_enemy_health <= 0:
                self.state.current_enemy_health = 0
                self.log_event(f"⚔️ Attacked with {played_card.name} for {played_card.current_value} damage! Enemy defeated!")
            else:
                self.log_event(f"⚔️ Attacked with {played_card.name} for {played_card.current_value} damage! Enemy health: {self.state.current_enemy_health}")
        
        return True

    def add_card_to_deck(self, card_name: str) -> bool:
        """
        Add a card to the player's personal deck by name.
        
        Args:
            card_name (str): The name of the card to add.
            
        Returns:
            bool: True if card was added successfully, False if card not found.
        """
        # Get card data from database
        card_data = get_card_by_name(card_name)
        
        if not card_data:
            self.log_event(f"⚠️ Card '{card_name}' not found in database!")
            return False
        
        # Create Card object
        name, deck_type, value, category, description = card_data
        new_card = Card(name, deck_type, value, category, description)
        
        # Add to player's personal deck
        self.state.player_deck.append(new_card)
        self.log_event(f"🎴 Added '{card_name}' to your deck!")
        
        return True
    
    def get_player_deck_names(self) -> List[str]:
        """
        Get a list of card names currently in the player's deck.
        
        Returns:
            List[str]: List of card names in the player's deck.
        """
        return [card.name for card in self.state.player_deck]

    def handle_draw_action(self) -> bool:
        """
        Handle paid draw action: spend 1 energy to draw 1 card from Main and Resource decks.
        
        Returns:
            bool: True if draw was successful, False if not enough energy.
        """
        if self.state.energy >= 1:
            # Subtract 1 energy
            self.state.energy -= 1
            
            # Draw 1 card from Main deck
            if "Main" in self.state.decks:
                self.state.player.draw_from(self.state.decks["Main"], 1)
            
            # Draw 1 card from Resource deck
            if "Resource" in self.state.decks:
                self.state.player.draw_from(self.state.decks["Resource"], 1)
            
            # Log the action
            self.log_event("Spent 1 energy to draw cards.")
            return True
        else:
            self.log_event("⚠️ Not enough energy to draw!")
            return False
    
    def __repr__(self) -> str:
        """
        Return string representation of the game controller.
        
        Returns:
            str: Information about the controller and its state.
        """
        return f"GameController({self.state})"


if __name__ == "__main__":
    # Example usage
    from .card import Card
    
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
