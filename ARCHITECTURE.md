# Project: Three-Deck Card Game Architecture (V6.0 - SQLite Integration)

## 1. Core Vision
A single-player virtual card game centered around a **Three-Deck System**. The project utilizes a strict Model-View-Controller (MVC) pattern. Version 6.0 replaces hardcoded card lists with a persistent SQLite database, enabling scalable data management and professional-grade state initialization.

---

## 2. Technical Architecture

### **The Resolution Engine** (`game_state.py`)
The Controller utilizes **Category-based logic** to resolve effects based on card data retrieved from the database:
* **The Model (`GameState`)**: 
    - Tracks `player.life_total` (starts at 20).
    - Tracks `state.energy` (resets to 5 each turn).
    - Tracks `state.current_enemy_health` (starts at 30).
* **Category Logic**: 
    - **Attack**: Subtracts `current_value` from `current_enemy_health`.
    - **Healing**: Adds `current_value` to `player.life_total`.
    - **Resource**: Adds `current_value` to `state.energy`.

### **The Component Structure (MVC + Database)**
* **The Model & Controller (`game_state.py`)**: The Brain. Manages the "Resolution Engine" and all numerical state modifications.
* **The Database Layer (`database_manager.py`)**: The Vault. Handles the SQLite connection, table creation (`cards` table), and initial data seeding.
* **The Factory (`game_factory.py`)**: The Hydrator. Connects to SQLite and executes SQL queries to fetch card attributes. It "hydrates" Python `Card` objects from the database rows to populate the decks.
* **The View (`main.py` & CLI logic)**: The Face. Remains UI-agnostic; it simply displays the state and captures inputs.

---

## 3. High-Level Game Flow (The SQL Loop)

1.  **Initialization**: 
    - `main.py` calls `game_factory.setup_game()`.
    - The Factory utilizes `database_manager.py` to ensure the SQLite database is ready.
    - A `SELECT * FROM cards` query retrieves the card library.
2.  **Refresh Phase**: UI displays Player Health, 30 HP Boss Health, Energy, and the `message_log`.
3.  **Resolution Phase**:
    - **Player Turn**: Attack cards reduce the persistent `current_enemy_health`.
    - **Enemy Turn**: An Encounter card is drawn; its value is dealt as damage to the player.
4.  **Game End Conditions**:
    - **Victory**: `state.current_enemy_health <= 0`.
    - **Defeat**: `player.life_total <= 0`.