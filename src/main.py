"""Main entry point for the three-deck virtual card game."""

from card import Card
from deck import Deck
from player import Player


def main():
    """Main game function."""
    print("Three-Deck Virtual Card Game")
    print("=" * 40)
    
    # Create some example cards
    cards = [
        Card("Fireball", "Spell Deck", 5, "Deal 5 damage to any target."),
        Card("Heal", "Spell Deck", 3, "Restore 3 health."),
        Card("Lightning Bolt", "Spell Deck", 7, "Deal 7 damage to any target."),
        Card("Shield", "Defense Deck", 4, "Block 4 damage."),
        Card("Sword Strike", "Attack Deck", 6, "Deal 6 damage."),
    ]
    
    # Create and shuffle deck
    deck = Deck(cards)
    print(f"Created deck: {deck}")
    
    deck.shuffle()
    print(f"After shuffle: {deck}")
    
    # Create players
    player1 = Player("Alice")
    player2 = Player("Bob")
    
    print(f"Created players: {player1}, {player2}")
    
    # Draw some cards for demonstration
    drawn_cards = deck.draw(3)
    player1.hand.extend(drawn_cards)
    
    print(f"{player1.name} drew {len(drawn_cards)} cards:")
    for card in drawn_cards:
        print(f"  {card}")
    
    print(f"Deck state: {deck}")
    
    # Create a discard deck for the player
    player1_discard = Deck()
    print(f"\n{player1.name}'s discard deck: {player1_discard}")
    
    # Demonstrate playing a card
    if player1.hand:
        print(f"\n{player1.name}'s current hand:")
        for i, card in enumerate(player1.hand):
            print(f"  [{i}] {card}")
        
        # Play the first card (index 0)
        played_card = player1.play_card(0, player1_discard)
        print(f"\n{player1.name} played: {played_card}")
        print(f"{player1.name}'s hand after playing: {player1}")
        print(f"{player1.name}'s discard deck after play: {player1_discard}")
        print(f"Cards in discard pile:")
        for card in player1_discard.discard_pile:
            print(f"  {card}")


if __name__ == "__main__":
    main()
