"""Player class for a three-deck virtual card game."""

from typing import List, Optional
from card import Card
from deck import Deck


class Player:
    """
    Represents the primary agent in the three-deck card game.
    
    Attributes:
        name (str): Player's name.
        hand (List[Card]): A list of Card objects currently held by the player.
        resource_level (int): Available energy for playing cards.
        life_total (int): Player's health points (starts at 20).
    """
    
    def __init__(self, name: str = "Player", life_total: int = 20, resource_level: int = 0) -> None:
        """
        Initialize a Player instance.
        
        Args:
            name (str, optional): Player's name. Defaults to "Player".
            life_total (int, optional): Starting health points. Defaults to 20.
            resource_level (int, optional): Starting energy/resources. Defaults to 0.
        """
        self.name = name
        self.hand: List[Card] = []
        self.resource_level = resource_level
        self.life_total = life_total
    
    def draw_from(self, deck: Deck, count: int = 1) -> List[Card]:
        """
        Draw cards from the provided deck and add them to the player's hand.
        
        Args:
            deck (Deck): The deck to draw from.
            count (int): Number of cards to draw. Defaults to 1.
            
        Returns:
            List[Card]: The drawn cards. May be fewer than requested if the deck is empty.
        """
        drawn_cards = deck.draw(count)
        self.hand.extend(drawn_cards)
        return drawn_cards
    
    def play_card(self, card_index: int, discard_to_deck: Deck) -> Optional[Card]:
        """
        Play a card from hand and move it to the discard pile.
        
        Args:
            card_index (int): Index of the card in hand to play.
            discard_to_deck (Deck): The deck where the card will be discarded.
            
        Returns:
            Optional[Card]: The played card, or None if index is invalid.
            
        Raises:
            IndexError: If card_index is out of range.
        """
        if 0 <= card_index < len(self.hand):
            card = self.hand.pop(card_index)
            discard_to_deck.add_to_discard([card])
            return card
        return None
    
    def modify_resource(self, amount: int) -> None:
        """
        Safely add or subtract from the resource level.
        
        Args:
            amount (int): Amount to add (positive) or subtract (negative).
        """
        self.resource_level += amount
        if self.resource_level < 0:
            self.resource_level = 0
    
    def __repr__(self) -> str:
        """
        Return string representation of the player.
        
        Returns:
            str: Information about player's hand size, resources, and life.
        """
        return f"Player(Hand: {len(self.hand)} cards, Resources: {self.resource_level}, Life: {self.life_total})"


if __name__ == "__main__":
    # Test simulation
    from card import Card
    
    # Initialize a player and a test deck
    player = Player(life_total=20, resource_level=5)
    
    test_cards = [
        Card("Fireball", "Spell Deck", 3, "Deal 3 damage"),
        Card("Heal", "Spell Deck", 2, "Restore 2 health"),
        Card("Lightning", "Spell Deck", 4, "Deal 4 damage")
    ]
    
    test_deck = Deck(test_cards)
    discard_deck = Deck()
    
    print(f"Initial player: {player}")
    print(f"Initial deck: {test_deck}")
    
    # Drawing a card into the hand
    drawn_cards = player.draw_from(test_deck)
    print(f"\nDrew {len(drawn_cards)} card(s): {drawn_cards}")
    print(f"Player after draw: {player}")
    print(f"Deck after draw: {test_deck}")
    
    # Drawing multiple cards
    drawn_more = player.draw_from(test_deck, 2)
    print(f"\nDrew {len(drawn_more)} more cards: {drawn_more}")
    print(f"Player after drawing more: {player}")
    print(f"Deck after drawing more: {test_deck}")
    
    # Playing that card to see it move to the discard pile
    if player.hand:
        played_card = player.play_card(0, discard_deck)
        print(f"\nPlayed card: {played_card}")
        print(f"Player after play: {player}")
        print(f"Discard deck after play: {discard_deck}")
    
    # Test resource modification
    print(f"\nBefore resource change: {player.resource_level}")
    player.modify_resource(-2)
    print(f"After losing 2 resources: {player.resource_level}")
    player.modify_resource(3)
    print(f"After gaining 3 resources: {player.resource_level}")
