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
        * `resolve_enemy_turn()`: Handles Encounter deck logic and player damage.
        * **Effect Resolution**: Interprets card descriptions to update player stats or deck states.

### **Encounter System (Enemy Turn)**
* **Responsibility**: Managed entirely by the `GameController`.
* **Logic Isolation**: The `Player` class remains unaware of the enemy; it only receives damage updates from the Controller.
* **Flow**: 
    1. Draw one card from the `Encounter` deck.
    2. Interpret the `current_value` as "Damage".
    3. Apply damage to `player.life_total`.
    4. Discard the encounter card back to the Encounter-specific discard pile.

---

## 3. High-Level Game Flow (The Alpha Loop - V2)

The **Heartbeat** of the game is located in `main.py`, which acts as the User Interface (UI) layer.

1.  **Player Phase**:
    * **Action**: Player plays cards using `energy`.
    * **End Turn**: Player triggers the transition by entering the 'e' command.
2.  **Encounter Phase**:
    * **Trigger**: Controller calls `resolve_enemy_turn()`.
    * **Result**: UI displays the enemy's name and the damage dealt to the player.
3.  **Reset Phase**:
    * **Trigger**: Controller calls `start_turn()`.
    * **Result**: Energy is reset, turn number increments, and the loop returns to the Player Phase.

---

## 4. Roadmap / Future Development
* **Visual UI**: Moving from terminal print statements to a Pygame-based window.
* **Rules Engine**: Moving complex card logic into a dedicated `rules.py` for easier balancing.