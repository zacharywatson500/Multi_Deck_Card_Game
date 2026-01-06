# Project: Three-Deck Card Game Architecture

## 1. Core Vision
A single-player virtual card game centered around a **Three-Deck System**. The game focuses on strategic deck management where cards cycle through individual Draw and Discard piles independently.

---

## 2. Technical Architecture

### **Card System** (`card.py`)
Defines the base unit of the game.
* **Attributes**: Name, Type, Cost, and Description/Effect.
* **Status**: **Complete**

### **Deck System** (`deck.py`)
Manages the lifecycle of card groups. This class is instantiated three times (one for each game deck).
* **Attributes**: 
    * `cards`: The current draw pile (List).
    * `discard_pile`: Cards waiting to be recycled (List).
    * `original_cards`: A master list for game resets.
* **Key Mechanics**:
    * **Automatic Cycling**: If a draw is requested and the draw pile is empty, the class automatically moves the discard pile to the draw pile and shuffles.
    * **Multi-Draw Logic**: Supports drawing `n` cards at once, returning a list of `drawn_cards`.
    * **add_to_discard(cards)**: Accepts a single Card or a List[Card] and appends them to the `discard_pile`.
* **Status**: **Complete**

### **Player System** (`player.py`)
The primary agent controlled by the user.
* **Attributes**:
    * `hand`: Current cards available to play (List).
    * `resource_level`: Energy available for the current turn.
    * `life_total`: Player health (Starts at 20).
* **Behaviors**:
    * `draw_from(deck, count=1)`: Requests `count` cards from a specific Deck instance and extends them to the hand. (Validated)
    * `play_card(index, target_deck)`: 
        1. Validates the index exists in `hand`.
        2. Pops the card from `hand`.
        3. Calls `target_deck.add_to_discard(card)`.
        4. Returns the `Card` object (so the Game Controller can resolve effects).
* **Status**: **In Progress** (Focus: Implementing Play Logic)

---

## 3. High-Level Game Flow
1.  **Initialization**: Three distinct `Deck` instances are created (e.g., Main, Resource, and Special).
2.  **Turn Start**: Player draws a set number of cards from specific decks to populate the `hand`.
3.  **Action Phase**: Player selects a card by index. The card is removed from the hand, its effect resolves, and it is sent to the target deck's discard pile.
4.  **Cycling**: When any individual deck runs out, it shuffles its own discard pile back into its draw pile independently.

---

## 4. Roadmap / Future Development
* **Game Controller**: Master class to manage turn phases and win/loss conditions.
* **UI/GUI Layer**: Visualizing the hand and deck counts using a Python library (e.g., Pygame or Tkinter).