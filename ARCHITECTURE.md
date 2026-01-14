# Project: Three-Deck Card Game Architecture

## 1. Core Vision
A single-player virtual card game centered around a **Three-Deck System**. The game focuses on strategic deck management where cards cycle through individual Draw and Discard piles independently.

---

## 2. Technical Architecture

### **Data & Logic Foundation** (`game_state.py`)
This file houses the "Brain" of the game, utilizing a strict separation between data storage and rule execution.

* **GameState (The Model)**:
    * **Role**: A pure data container holding the current snapshot of the game.
    * **Attributes**: 
        * `decks`: A dictionary containing three `Deck` instances (Main, Resource, Encounter).
        * `player`: The active `Player` instance.
        * `turn_number`, `energy`, and `is_game_over` (Variable State).
* **GameController (The Referee)**:
    * **Role**: Executes game rules and modifies the `GameState`.
    * **Core Responsibilities**:
        * `start_turn()`: Increments turn, resets energy, and draws initial cards.
        * **Validation**: Ensures actions (like playing a card) are legal before modifying state.
        * **Effect Resolution**: Interprets card descriptions to update player stats or deck states.

### **Supporting Systems**
* **Card System** (`card.py`): Defines attributes for Name, Type, Cost, and Effect. **(Complete)**
* **Deck System** (`deck.py`): Handles draw/discard piles and automatic shuffling/cycling. **(Complete)**
* **Player System** (`player.py`): Manages the player's `hand`, `life_total`, and `resource_level`. **(Complete)**

---

## 3. High-Level Game Flow (The Alpha Loop)

The **Heartbeat** of the game is located in `main.py`, which acts as the User Interface (UI) layer.

1.  **Initialization**: 
    * Generate test cards and populate the `Main`, `Resource`, and `Encounter` decks.
    * Instantiate `GameState` and `GameController`.
2.  **The Interactive Loop (`while not is_game_over`)**:
    * **Display**: Print the current `GameState` (Hand, Health, Energy, and Deck sizes).
    * **Input**: Capture user commands (e.g., `d` for draw, `p` for play, `q` for quit).
    * **Action**: Pass valid commands to the `GameController` to update the `GameState`.
3.  **Turn Transition**: 
    * The loop resets for the next player action until an "End Turn" or "Quit" command is received.

---

## 4. Roadmap / Future Development
* **Visual UI**: Moving from terminal print statements to a Pygame-based window.
* **Rules Engine**: Moving complex card logic into a dedicated `rules.py` for easier balancing.