# Project: Quad-Deck Card Game Architecture (V9.0 - Streamlined Engine)

## 1. Core Vision
A single-player virtual card game centered around a **Quad-Deck System** with dynamic deck-building mechanics. The project utilizes a strict Model-View-Controller (MVC) pattern backed by a persistent SQLite database. Players start with specialized, separated decks and draft new cards from a global library to build an economic and combat engine capable of defeating scaling encounters.

---

## 2. Technical Architecture

### **The Resolution Engine** (`game_state.py`)
The Controller utilizes **Category-based logic** to resolve effects based on card data retrieved from the database. It manages four distinct dynamic array states for deck cycling:
* **The Model (`GameState`)**: 
    - Tracks `player.life_total` (starts at 20) and `state.energy` (resets to 5 each turn).
    - Tracks `state.current_enemy_health` (starts at 30, modified by Encounter cards).
    - **Deck States**: Manages separated arrays for `attack_deck`, `healing_deck`, and `resource_deck` (the active draw piles), an `encounter_deck` for the enemy, and `player_hand` (current playable options).
* **Category Logic**: 
    - **Attack**: Subtracts `current_value` from `current_enemy_health`.
    - **Healing**: Adds `current_value` to `player.life_total`.
    - **Resource**: Adds `current_value` to `state.energy`.

### **The Component Structure (MVC + Database Layer)**
* **The Model & Controller (`game_state.py`)**: The Brain. Manages the Resolution Engine, numerical modifications, and explicit draw sequence routing.
* **The Database Layer (`database_manager.py`)**: The Vault. Contains the `cards` table (`deck_type` strictly categorized into 'Attack', 'Healing', 'Resource', and 'Encounter'). Acts as the immutable "Global Library".
* **The Factory (`game_factory.py`)**: The Hydrator & Drafter. 
    - Executes initial `SELECT` queries to build specific starter decks populated exclusively from their respective database categories.
    - Executes Draft queries using `NOT IN` clauses to fetch valid upgrade options from the database.
* **The View (`main.py` & UI logic)**: The Face. Displays state (including granular deck counts), listens for input events, and presents the turn-end Drafting Menu without nested blocking loops.

---

## 3. High-Level Game Flow (The Engine Loop)

1.  **Initialization Phase**: 
    - `main.py` calls `game_factory.setup_game()`.
    - The Factory queries the database to "hydrate" the starting cards, sorting them explicitly into the four distinct deck arrays.
2.  **Combat Phase**:
    - **Player Turn**: 
        - **Automated Draw**: Player spends 1 Energy to trigger a frictionless draw action, automatically pulling exactly 1 card from the Attack, Healing, and Resource decks simultaneously.
        - **Play**: Player spends energy to play cards from hand, resolving category logic.
    - **Enemy Turn**: An Encounter card logic executes against the player.
3.  **Drafting Phase (State Evolution)**:
    - The Factory queries the database for random cards NOT currently in the player's deck arrays.
    - The player selects one card, which is instantiated and permanently added to the appropriate active