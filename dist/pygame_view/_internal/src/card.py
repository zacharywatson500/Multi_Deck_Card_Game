"""Card class for a three-deck virtual card game."""

from typing import Optional


class Card:
    """
    Represents a single card in a three-deck virtual card game.
    
    Attributes:
        name (str): The name of the card.
        deck_type (str): The deck this card belongs to.
        base_value (int): The permanent, starting value of the card.
        current_value (int): The value that changes during gameplay.
        description (str): A brief explanation of what the card does.
    """
    
    def __init__(
        self,
        name: str,
        deck_type: str,
        value: int,
        category: str = "Attack",
        description: Optional[str] = ""
    ) -> None:
        """
        Initialize a Card instance.
        
        Args:
            name (str): The name of the card.
            deck_type (str): To identify which of the three decks this card belongs to.
            value (int): The numerical power or cost of the card.
            category (str): The functional category of the card (Attack, Healing, Resource).
            description (str, optional): A brief explanation of what the card does.
                                        Defaults to an empty string.
        """
        self.name = name
        self.deck_type = deck_type
        self.base_value = value
        self.current_value = value
        self.category = category
        self.description = description.strip()
    
    def __repr__(self) -> str:
        """
        Return an unambiguous string representation of the card.
        
        Returns:
            str: Formatted string in the format: [Name | Deck: Type | Value: current_value (Base: base_value)]
        """
        return f"[{self.name} | Cat: {self.category} | Deck: {self.deck_type} | Value: {self.current_value} (Base: {self.base_value})]"
    
    def update_value(self, new_value: int) -> None:
        """
        Set the card's current_value to a specific number.
        
        Args:
            new_value (int): The new value to assign to the card.
        """
        if new_value < 0:
            new_value = 0
        self.current_value = new_value
    
    def adjust_value(self, amount: int) -> None:
        """
        Add or subtract from the current value.
        
        Args:
            amount (int): The amount to add (positive) or subtract (negative) from the current value.
        """
        self.current_value += amount
        if self.current_value < 0:
            self.current_value = 0
    
    def reset_value(self) -> None:
        """
        Reset current_value back to equal base_value.
        """
        self.current_value = self.base_value


if __name__ == "__main__":
    # Example usage
    example_card = Card(
        name="Fireball",
        deck_type="Spell Deck",
        value=5,
        description="Deal 5 damage to any target."
    )
    print(example_card) 
    example_card.update_value(10)
    print(f"After update: {example_card}")
    example_card.adjust_value(-3)
    print(f"After adjustment: {example_card}")
    example_card.reset_value()
    print(f"After reset: {example_card}")
