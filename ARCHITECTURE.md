# Project: Three-Deck Card Game Architecture

## 1. Core Vision
A single-player virtual card game centered around a **Three-Deck System**. The project utilizes a strict Model-View-Controller (MVC) pattern. The architecture is explicitly designed to be UI-agnostic, separating the core game logic from the visual display to allow for a seamless transition from a Command Line Interface (CLI) to a graphical interface (e.g., Pygame).

---

## 2. Technical Architecture

### **The Resolution Engine** (`game_state.py`)
The Controller utilizes **Category-based logic** rather than deck-based logic for resolving card effects:
* **Hybrid Support**: A single deck can contain multiple categories (Attack, Healing, Resource).
* **Category vs. Deck**: 
    - `card.category`: Dictates the **Effect** (math applied to life or energy).
    - `card.deck_type`: Dictates the **Discard Path** (integrity of individual piles).
* `resolve_card(index)`: Branches based on the category to apply healing, damage, or energy generation, acting as the Universal Resolver.

### **The Component Structure (MVC + Factory)**
* **The Model & Controller (`game_state.py`)**: The Brain. Owns the "Resolution Engine", maintains the data state (`GameState`), and handles all `player.life_total` and `state.energy` modifications (`GameController`).
* **The Factory (`game_factory.py`)**: The Builder. Strictly handles data initialization. It generates the hardcoded card pools, instantiates the decks and player, and returns a fully prepped `GameState` and `GameController`.
* **The View (`cli_interface.py`)**: The Face. A purely visual and input-handling layer. It reads the `message_log` and state variables to render the screen, and parses user commands to send to the Controller.
* **The Entry Point (`main.py`)**: The Application Runner. A minimalist file that simply calls the Factory to get the state/controller, and then passes them into the View's main game loop.

---

## 3. High-Level Game Flow (The Alpha Loop - V5.0 GUI Prep)

1.  **Initialization Phase (Run Once)**: `main.py` calls `game_factory.py` to build the world, then passes the keys to the UI loop.
2.  **Refresh Phase**: The UI (`cli_interface.py`) reads the current `GameState` and renders Player stats, Deck counts, and the `message_log`.
3.  **Input Phase**: The UI captures a command (e.g., `p 0`).
4.  **Resolution Phase**:
    * UI asks the Controller: "Can I play this?" (`controller.can_play_card`)
    * If yes, UI tells Controller to execute (`controller.resolve_card`).
    * Controller checks `category`:
        - **Healing**: Adds to Life, subtracts Energy.
        - **Attack**: Logs Damage, subtracts Energy.
        - **Resource**: Adds Energy (0 cost).
    * Controller updates the internal `message_log` and discards the card to its specific `card.deck_type` discard pile.
5.  **End Turn / Reset Phase**: The player ends their turn, triggering the enemy encounter resolution. The Controller then increments the turn counter and resets energy to **5**.