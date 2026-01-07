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
Manages the lifecycle of card groups.
* **Attributes**: 
    * `cards`: The current draw pile (List).
    * `discard_pile`: Cards waiting to be recycled (List).
    * `original_cards`: A master list for game resets.
* **Key Mechanics**:
    * **Automatic Cycling**: If a draw is empty, moves discard to draw and shuffles.
    * **add_to_discard(cards)**: Appends Card or List[Card] to the discard pile.
* **Status**: **Complete**

### **Player System** (`player.py`)
The primary agent controlled by the user.
* **Attributes**: `hand`, `resource_level`, `life_total`.
* **Behaviors**: `draw_from(deck, count)`, `play_card(index, target_deck)`.
* **Status**: **Complete**

### **Game Controller / State** (`main.py`)
The "Brain" that centralizes all game data and orchestrates interactions.
* **State Management**:
    * **Physical State**: Owns the 3 `Deck` instances (Main, Resource, Encounter) and the `Player` instance.
    * **Variable State**: Tracks `turn_number`, `current_energy`, and `is_game_over`.
    * **Phase State**: Tracks the current sub-turn phase (Start, Action, End).
* **Core Responsibilities**:
    * **Input Handling**: Translates user terminal commands into game actions.
    * **Effect Resolution**: Interprets card descriptions (e.g., if a card says "+2 Energy", the Controller updates the Player's `resource_level`).
    * **Win/Loss Validation**: Checks life totals and deck counts after every action.
* **Status**: **In Progress** (Next Implementation Goal)

---

## 3. High-Level Game Flow (The Turn Loop)

1. **Initialization**: 
    * Create `Main`, `Resource`, and `Encounter` decks.
    * Instantiate the `Player`.
2. **Turn Start Phase**: 
    * Increment `turn_number`.
    * Reset `resource_level`.
    * Player draws a fixed amount from designated decks.
3. **Action Phase (Looping)**: 
    * Display Hand and Stats.
    * Accept user input (Play index or End Turn).
    * Resolve Card effects and move played cards to appropriate discard piles.
4. **End Phase**: 
    * Resolve "End of Turn" effects.
    * Check for Win/Loss conditions.
5. **Cycling**: Individual decks shuffle their own discard piles back into their draw piles automatically when empty.

---

## 4. Roadmap / Future Development
* **Logic Rules Engine**: Moving card effect logic out of `main.py` and into a dedicated `rules.py`.
* **UI/GUI Layer**: Transitioning from terminal print statements to a visual window (Pygame).