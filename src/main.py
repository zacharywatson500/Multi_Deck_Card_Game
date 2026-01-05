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


if __name__ == "__main__":
    main()
