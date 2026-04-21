# Project: Quad-Deck Card Game Architecture (V11.0 - Pygame GUI Integration)

## 1. Core Vision
A single-player virtual card game centered around a **Quad-Deck System** with dynamic deck-building mechanics. The project utilizes a strict Model-View-Controller (MVC) pattern backed by a persistent SQLite database. Players start with specialized, separated decks and draft new cards from a global library to build an economic and combat engine capable of defeating scaling encounters. 

*Theme Note:* The game utilizes a lighthearted, family-friendly Sci-Fi/Steampunk aesthetic (e.g., "Plasma Blast", "Clockwork Scout", "Flying Hospital").

---

## 2. Technical Architecture & File Structure

### **The Resolution Engine** (`src/game_state.py`)
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
* **The Model & Controller (`src/game_state.py`)**: The Brain. Manages the Resolution Engine, explicit draw sequence routing, and prepares Draft options (ensuring the View remains logic-blind).
* **The Database Layer (`src/database_manager.py`)**: The Vault. Contains the `cards` table (`deck_type` strictly categorized into 'Attack', 'Healing', 'Resource', and 'Encounter'). Acts as the immutable "Global Library".
* **The Factory (`src/game_factory.py`)**: The Hydrator & Drafter. Executes initial `SELECT` queries to build starter decks populated exclusively from their respective database categories.
* **The View (`pygame_view.py`)**: The Face. A Frame-Driven graphical interface powered by Pygame-CE. It queries the Controller at 60 FPS to render the current game state to the screen. 
* **Assets & Tools**: Database initialization is isolated in `scripts/seed_db.py`, and visual assets are staged in `assets/images/`.

---

## 3. High-Level Game Flow (The Engine Loop)

1.  **Initialization Phase**: 
    - The Factory queries the database to "hydrate" the starting cards, sorting them explicitly into the four distinct deck arrays.
2.  **Combat Phase**:
    - **Player Turn**: 
        - **Automated Draw**: Player spends 1 Energy to trigger a frictionless draw action, automatically pulling exactly 1 card from the Attack, Healing, and Resource decks simultaneously.
        - **Play**: Player spends energy to play cards from hand, resolving category logic.
    - **Enemy Turn**: An Encounter card logic executes against the player.
3.  **Drafting Phase (State Evolution)**:
    - The Controller queries the database for exactly 1 random card from each player category (Attack, Healing, Resource) NOT currently in the player's deck arrays.
    - The player selects one card, which is instantiated and permanently added to the appropriate active deck for future turns.
4.  **Game End Conditions**:
    - **Victory**: `state.current_enemy_health <= 0`.
    - **Defeat**: `player.life_total <= 0`.

---

## 4. Pygame GUI Implementation

The project has transitioned from a CLI (`main.py`) to a Frame-Driven desktop application using **Pygame-CE**.

### **Visual Organization**
* **The HUD**: Player stats (Health, Energy) and Enemy stats are pinned to the top of the screen.
* **The Hand**: Cards are rendered as rounded rectangles at the bottom of the screen. They are sorted dynamically:
  1.  Primarily by **Category** (Resource -> Attack -> Healing).
  2.  Secondarily by **Value** (Highest to Lowest). 

### **Color Palette Standards**
To ensure immediate player recognition, UI elements and Card backgrounds strictly adhere to the following category color codes:
* **Attack**: Red `(255, 85, 85)`
* **Healing**: Green `(85, 255, 85)`
* **Resource**: Blue `(85, 85, 255)`
* **Encounter/Enemy**: Black/Charcoal `(51, 51, 51)`
* **Background**: Dark Modern Grey `(30, 30, 40)`

### **Interaction Paradigm**
The application relies on a 60 FPS Game Loop. Player inputs (keyboard presses or mouse clicks) are intercepted by the Pygame Event Queue and routed to the `GameController` to mutate the state, which is immediately reflected in the next frame draw.