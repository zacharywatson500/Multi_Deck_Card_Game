"""Deck class for managing cards in a three-deck virtual card game."""

import random
from typing import List, Optional
from card import Card


class Deck:
    """
    Represents a deck of cards that can be shuffled, drawn from, and managed.
    
    Attributes:
        cards (List[Card]): The list of cards currently in the deck.
        discard_pile (List[Card]): Cards that have been played/discarded.
        original_cards (List[Card]): The original set of cards for reset purposes.
    """
    
    def __init__(self, cards: Optional[List[Card]] = None) -> None:
        """
        Initialize a Deck instance.
        
        Args:
            cards (List[Card], optional): Initial list of cards. If None, starts empty.
        """
        self.cards = cards.copy() if cards else []
        self.discard_pile: List[Card] = []
        self.original_cards = self.cards.copy()
    
    def shuffle(self) -> None:
        """
        Shuffle the deck randomly.
        """
        random.shuffle(self.cards)
    
    def draw(self, count: int = 1) -> List[Card]:
        """
        Draw cards from the top of the deck.
        
        Args:
            count (int): Number of cards to draw. Defaults to 1.
            
        Returns:
            List[Card]: The drawn cards. May be fewer than requested if both deck and discard pile are empty.
            
        Raises:
            ValueError: If count is less than 1.
        """
        if count < 1:
            raise ValueError("Must draw at least 1 card")
        
        drawn_cards = []
        cards_to_draw = count
        
        while cards_to_draw > 0:
            if self.cards:
                drawn_cards.append(self.cards.pop(0))
                cards_to_draw -= 1
            else:
                if self.discard_pile:
                    self.cards = self.discard_pile.copy()
                    self.discard_pile.clear()
                    self.shuffle()
                else:
                    break
        
        return drawn_cards
    
    def add_to_discard(self, cards) -> None:
        """
        Add cards to the discard pile.
        
        Args:
            cards: Either a single Card or List[Card] to add to discard pile.
        """
        if isinstance(cards, list):
            self.discard_pile.extend(cards)
        else:
            self.discard_pile.append(cards)
    
    def reset(self) -> None:
        """
        Reset the deck to its original state, clearing discard pile.
        """
        self.cards = self.original_cards.copy()
        self.discard_pile.clear()
    
    def __len__(self) -> int:
        """
        Return the number of cards remaining in the deck.
        
        Returns:
            int: Number of cards in deck.
        """
        return len(self.cards)
    
    def __repr__(self) -> str:
        """
        Return string representation of the deck.
        
        Returns:
            str: Information about deck size and discard pile size.
        """
        return f"Deck({len(self.cards)} cards, {len(self.discard_pile)} in discard)"


if __name__ == "__main__":
    # Example usage
    from .card import Card
    
    test_cards = [
        Card("Fireball", "Spell Deck", 5, "Deal 5 damage"),
        Card("Heal", "Spell Deck", 3, "Restore 3 health"),
        Card("Lightning", "Spell Deck", 7, "Deal 7 damage")
    ]
    
    deck = Deck(test_cards)
    print(f"Initial deck: {deck}")
    
    deck.shuffle()
    print(f"After shuffle: {deck}")
    
    drawn = deck.draw(2)
    print(f"Drew {len(drawn)} cards: {drawn}")
    print(f"Deck after draw: {deck}")
    
    deck.add_to_discard(drawn)
    print(f"After adding to discard: {deck}")
    
    deck.reset()
    print(f"After reset: {deck}")
