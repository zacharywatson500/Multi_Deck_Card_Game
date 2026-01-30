
"""Main entry point for the three-deck virtual card game."""

import os
import sys
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
        Card("Fireball", "Main", 3, "Deal 3 damage to enemy"),
        Card("Sword Strike", "Main", 2, "Deal 2 damage to enemy"),
        Card("Lightning Bolt", "Main", 4, "Deal 4 damage to enemy"),
        Card("Ice Shard", "Main", 2, "Deal 2 damage to enemy"),
        Card("Arrow Shot", "Main", 1, "Deal 1 damage to enemy")
    ]
    
    # Energy cards for "Resource" deck
    resource_cards = [
        Card("Energy Crystal", "Resource", 1, "Gain 1 energy"),
        Card("Mana Potion", "Resource", 2, "Gain 2 energy"),
        Card("Power Gem", "Resource", 3, "Gain 3 energy"),
        Card("Focus Charm", "Resource", 1, "Gain 1 energy"),
        Card("Meditation", "Resource", 2, "Gain 2 energy")
    ]
    
    # Enemy cards for "Encounter" deck
    enemy_cards = [
        Card("Goblin", "Encounter", 2, "Enemy with 2 health"),
        Card("Orc", "Encounter", 4, "Enemy with 4 health"),
        Card("Dragon", "Encounter", 8, "Enemy with 8 health"),
        Card("Skeleton", "Encounter", 1, "Enemy with 1 health"),
        Card("Troll", "Encounter", 6, "Enemy with 6 health")
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
    
    return game_state, game_controller


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_ui(state: GameState) -> None:
    """
    Display the current game UI showing turn, player stats, and deck info.
    
    Args:
        state (GameState): The current game state.
    """
    print("=" * 50)
    print(f"TURN {state.turn_number}")
    print("=" * 50)
    print(f"Player Health: {state.player.life_total}")
    print(f"Energy: {state.energy}")
    print("\nDeck Status:")
    print(f"  Main Deck: {len(state.decks['Main'])} cards remaining")
    print(f"  Resource Deck: {len(state.decks['Resource'])} cards remaining")
    print(f"  Encounter Deck: {len(state.decks['Encounter'])} cards remaining")
    print("=" * 50)


def display_hand(player: Player) -> None:
    """
    Display the cards currently in the player's hand.
    
    Args:
        player (Player): The player whose hand to display.
    """
    print("\nYOUR HAND:")
    if not player.hand:
        print("  (No cards in hand)")
    else:
        for i, card in enumerate(player.hand):
            print(f"  [{i}] {card.name} (Cost: {card.current_value}) - {card.description}")
    print()


def handle_input(state: GameState, controller: GameController) -> None:
    """
    Handle user input for the game.
    
    Args:
        state (GameState): The current game state.
        controller (GameController): The game controller.
    """
    while True:
        try:
            user_input = input("Enter command (d=draw, p [index]=play, e=end turn, q=quit): ").strip().lower()
            
            if not user_input:
                continue
                
            if user_input == 'd':
                # Start turn: draw cards and reset energy
                controller.start_turn()
                print("Cards drawn! Energy reset to 3.")
                break
                
            elif user_input == 'e':
                # End turn: resolve enemy encounter and start next turn
                enemy_card = controller.resolve_enemy_turn()
                if enemy_card:
                    print(f"The {enemy_card.name} attacks for {enemy_card.current_value} damage!")
                    # Automatically start next turn
                    controller.start_turn()
                    print("New turn started! Cards drawn and energy reset to 3.")
                else:
                    print("No enemy cards remaining!")
                break
                
            elif user_input == 'q':
                # Quit game
                state.is_game_over = True
                print("Game ended.")
                break
                
            elif user_input.startswith('p '):
                # Play card
                try:
                    parts = user_input.split()
                    if len(parts) != 2:
                        print("Usage: p [index]")
                        continue
                        
                    card_index = int(parts[1])
                    
                    if card_index < 0 or card_index >= len(state.player.hand):
                        print(f"Invalid card index. Must be between 0 and {len(state.player.hand) - 1}")
                        continue
                    
                    card = state.player.hand[card_index]
                    
                    # Check if player has enough energy
                    if state.energy < card.current_value:
                        print(f"Not enough energy! Need {card.current_value}, have {state.energy}")
                        continue
                    
                    # Play the card
                    played_card = state.player.play_card(card_index, state.decks["Main"])
                    if played_card:
                        state.energy -= played_card.current_value
                        print(f"Played {played_card.name}! Energy remaining: {state.energy}")
                        
                        # Simple damage logic for attack cards
                        if played_card.deck_type == "Main":
                            print(f"Dealt {played_card.current_value} damage to enemy!")
                        elif played_card.deck_type == "Resource":
                            print(f"Gained {played_card.current_value} energy!")
                            # For resource cards, add the energy back (they represent energy gain)
                            state.energy += played_card.current_value
                    break
                    
                except ValueError:
                    print("Invalid card index. Please enter a number.")
                    continue
                    
            else:
                print("Unknown command. Use 'd', 'p [index]', 'e', or 'q'.")
                continue
                
        except KeyboardInterrupt:
            print("\nGame interrupted.")
            state.is_game_over = True
            break
        except Exception as e:
            print(f"Error: {e}")
            continue


def main() -> None:
    """Main game loop."""
    # Set up the game
    state, controller = setup_game()
    
    print("Welcome to the Three-Deck Card Game!")
    print("Commands:")
    print("  d     - Draw cards and start new turn")
    print("  p [n] - Play card at index n from hand")
    print("  e     - End turn (enemy attacks, then new turn starts)")
    print("  q     - Quit game")
    print("\nPress Enter to start...")
    input()
    
    # Main game loop
    while not state.is_game_over:
        # Clear screen and display UI
        clear_screen()
        display_ui(state)
        display_hand(state.player)
        
        # Handle user input
        handle_input(state, controller)
        
        # Check for game over conditions
        if state.player.life_total <= 0:
            state.is_game_over = True
            print("Game Over! You have been defeated.")
        elif len(state.decks["Main"]) == 0 and len(state.decks["Resource"]) == 0:
            state.is_game_over = True
            print("Game Over! All decks are empty.")
    
    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
