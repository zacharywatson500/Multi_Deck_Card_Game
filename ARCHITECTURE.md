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
        * `message_log`: A list of strings tracking the chronological history of game events.

* **GameController (The Referee)**:
    * **Role**: Executes game rules and serves as the primary "Journalist" for the state.
    * **Core Responsibilities**:
        * `start_turn()`: Increments turn number, resets energy to **5**, and logs the start of a new turn.
        * `handle_draw_action()`: **(New)** Checks for 1 available energy to draw one card from all active decks (Main, Resource).
        * `resolve_enemy_turn()`: Processes the Encounter deck logic and logs attack results.
        * `log_event()`: Centralized method to push strings into the `GameState.message_log`.

### **The Energy Economy**
* **Turn Start**: Energy resets to a base of **5**.
* **Resource Management**: 
    * **Drawing**: Costs **1 energy** per draw action.
    * **Playing**: Costs energy equal to the card's `current_value`.
* **Tactical Choice**: Players must balance spending energy on gathering new cards (Drawing) versus executing their current hand (Playing).

---

## 3. High-Level Game Flow (The Alpha Loop - V4)

The **Heartbeat** is located in `main.py`, which acts as the User Interface (UI) layer.

1.  **Refresh Phase**:
    * UI calls `clear_screen()` and renders Player stats and recent `message_log` entries.
2.  **Player Phase (The Decision Loop)**:
    * **Play Card**: Costs energy; card logic is resolved.
    * **Draw Card**: Costs **1 energy**; adds new cards to hand via `handle_draw_action()`.
3.  **Encounter Phase**:
    * Triggered explicitly by the 'e' command.
    * Controller resolves the enemy attack and adds it to the log.
4.  **Reset Phase**:
    * Controller triggers `start_turn()` to reset energy and the loop returns to the Refresh Phase.

---

## 4. Roadmap / Future Development
* **Card Limit**: Implementing a maximum hand size to prevent "over-drawing".
* **Visual UI**: Transitioning to Pygame for a graphical representation.
* **Rules Engine**: Advanced card effects (Healing, Buffs).