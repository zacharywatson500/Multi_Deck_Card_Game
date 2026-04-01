
"""Main entry point for the three-deck virtual card game."""

import os
import sys
from src.player import Player

from src.game_factory import setup_game
from src.game_state import GameState, GameController


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_ui(state: GameState) -> None:
    """
    Display the current game UI showing turn, player stats, deck info, and recent events.
    
    Args:
        state (GameState): The current game state.
    """
    print("=" * 50)
    print(f"TURN {state.turn_number}")
    print("=" * 50)
    print(f"Player Health: {state.player.life_total} | Enemy Health: {state.current_enemy_health}")
    print(f"Energy: {state.energy}")
    print("\nDeck Status:")
    print(f"  Main Deck: {len(state.decks['Main'])} cards remaining")
    print(f"  Resource Deck: {len(state.decks['Resource'])} cards remaining")
    print(f"  Encounter Deck: {len(state.decks['Encounter'])} cards remaining")
    
    # Show recent events
    print("\nRECENT EVENTS:")
    recent_events = state.message_log[-5:]  # Get last 5 messages
    for event in recent_events:
        print(f"  {event}")
    
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
                # Paid draw action
                controller.handle_draw_action()
                break
                
            elif user_input == 'e':
                # End turn: resolve enemy encounter and start next turn
                enemy_card = controller.resolve_enemy_turn()
                if enemy_card:
                    # Automatically start next turn
                    controller.start_turn()
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
                    
                    # Use controller.can_play_card for validation
                    if not controller.can_play_card(card_index):
                        if card_index < 0 or card_index >= len(state.player.hand):
                            print(f"Invalid card index. Must be between 0 and {len(state.player.hand) - 1}")
                        else:
                            card = state.player.hand[card_index]
                            print(f"Not enough energy! Need {card.current_value}, have {state.energy}")
                        continue

                    # Store card reference before playing it
                    card = state.player.hand[card_index]
                    
                    # If validation passes, call controller.resolve_card
                    if controller.resolve_card(card_index):
                        if card.category == "Resource":
                            action_message = f"Gained {card.current_value} energy!"
                        elif card.category == "Healing":
                            action_message = f"Healed {card.current_value} health!"
                        else:  # Attack category
                            action_message = f"Dealt {card.current_value} damage to enemy!"
                        print(f"Played {card.name}!: {action_message}") 
                        print(f"Energy remaining: {state.energy}")
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
    print("  d     - Draw cards (costs 1 energy)")
    print("  p [n] - Play card at index n from hand")
    print("  e     - End turn (enemy attacks, then new turn starts)")
    print("  q     - Quit game")
    
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
        elif state.current_enemy_health <= 0:
            state.is_game_over = True
            print("Victory! The Boss has been defeated!")
    
    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
