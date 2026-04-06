# Project: Tri-Deck Card Game Architecture (V7.0 - Deck-Builder Transition)

## 1. Core Vision
A single-player virtual card game centered around a **Three-Deck System** with dynamic deck-building mechanics. The project utilizes a strict Model-View-Controller (MVC) pattern and is backed by a persistent SQLite database. Players start with a minimal deck and draft new cards from a global library to build an economic and combat engine capable of defeating scaling encounters.

---

## 2. Technical Architecture

### **The Resolution Engine** (`game_state.py`)
The Controller utilizes **Category-based logic** to resolve effects based on card data retrieved from the database. It now manages dynamic array states for deck cycling:
* **The Model (`GameState`)**: 
    - Tracks `player.life_total` (starts at 20) and `state.energy` (resets to 5 each turn).
    - Tracks `state.current_enemy_health` (starts at 30, modified by encounter cards).
    - **Deck State**: Manages `player_deck` (active draw pile), `player_hand` (current playable options), and `discard_pile` (used cards awaiting reshuffle).
* **Category Logic**: 
    - **Attack**: Subtracts `current_value` from `current_enemy_health`.
    - **Healing**: Adds `current_value` to `player.life_total`.
    - **Resource**: Adds `current_value` to `state.energy`.

### **The Component Structure (MVC + Database)**
* **The Model & Controller (`game_state.py`)**: The Brain. Manages the Resolution Engine, numerical modifications, and deck array cycling (drawing, discarding, reshuffling).
* **The Database Layer (`database_manager.py`)**: The Vault. Contains the `cards` table and acts as the immutable "Global Library" for all possible game content.
* **The Factory (`game_factory.py`)**: The Hydrator & Drafter. 
    - Executes initial `SELECT` queries with `ORDER BY RANDOM() LIMIT 5` to build starter decks.
    - Executes Draft queries using `NOT IN` clauses to fetch valid upgrade options.
* **The View (`main.py` & UI logic)**: The Face. Displays state, captures input, and presents the turn-end Drafting Menu.

---

## 3. High-Level Game Flow (The Engine Loop)

1.  **Initialization Phase**: 
    - `main.py` calls `game_factory.setup_game()`.
    - The Factory queries the database to "hydrate" 5 starting cards for the player and the enemy.
2.  **Combat Phase**:
    - **Player Turn**: Player draws a hand, spends energy to play cards, resolving category logic. Remaining hand and played cards go to the discard pile.
    - **Enemy Turn**: An Encounter card logic executes against the player.
3.  **Drafting Phase (State Evolution)**:
    - The Factory queries the database for 3 random cards NOT currently in the player's deck array.
    - The player selects one card, which is instantiated and added to their `discard_pile` or `player_deck` for future turns.
4.  **Game End Conditions**:
    - **Victory**: `state.current_enemy_health <= 0`.
    - **Defeat**: `player.life_total <= 0`.