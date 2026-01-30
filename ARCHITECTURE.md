# Project: Three-Deck Card Game Architecture

## 1. Core Vision
A single-player virtual card game centered around a **Three-Deck System**. The game focuses on strategic deck management where cards cycle through individual Draw and Discard piles independently.

---

## 2. Technical Architecture

### **Data & Logic Foundation** (`game_state.py`)
This file houses the "Brain" of the game, utilizing a strict separation between data storage and rule execution.

* **GameState (The Model)**:
    * **Role**: A data container holding the current snapshot and history of the game.
    * **Attributes**: 
        * `decks`: Dictionary of three `Deck` instances (Main, Resource, Encounter).
        * `player`: The active `Player` instance.
        * `turn_number`, `energy`, `is_game_over`.
        * **`message_log` (New)**: A list of strings tracking the chronological history of game events (e.g., "Player played Fireball", "Orc attacked for 4 damage").

* **GameController (The Referee)**:
    * **Role**: Executes game rules and serves as the primary "Journalist" for the state.
    * **Core Responsibilities**:
        * `start_turn()`: Resets energy, draws cards, and logs the start of a new turn.
        * `resolve_enemy_turn()`: Processes the Encounter deck logic and logs attack results.
        * **`log_event()` (New)**: Centralized method to push strings into the `GameState.message_log`.

### **Encounter System (Enemy Turn)**
* **Responsibility**: Managed entirely by the `GameController`.
* **Logic Isolation**: The `Player` class only receives damage updates; the Controller handles the deck interaction.
* **Flow**: 
    1. Draw one card from the `Encounter` deck.
    2. Apply `current_value` as damage to `player.life_total`.
    3. Discard the encounter card to its specific discard pile.
    4. **Persistence**: The attack details are saved to the `message_log` so they survive the screen refresh.

---

## 3. High-Level Game Flow (The Alpha Loop - V3)

The **Heartbeat** is located in `main.py`, which acts as the User Interface (UI) layer.

1.  **Refresh Phase**:
    * UI calls `clear_screen()`.
    * UI renders Player stats and the most recent entries from the `message_log`.
2.  **Player Phase**:
    * Player plays cards or draws.
    * Actions are passed to the Controller, which updates the state and the log.
3.  **Encounter Phase**:
    * Triggered by the 'e' command.
    * Controller resolves the enemy attack and adds it to the log.
4.  **Reset Phase**:
    * Controller triggers `start_turn()` and the loop returns to the Refresh Phase.

---

## 4. Roadmap / Future Development
* **Visual UI**: Transitioning to Pygame for a graphical representation of the logs and cards.
* **Rules Engine**: Advanced card effects (Healing, Buffs) handled by the Controller.