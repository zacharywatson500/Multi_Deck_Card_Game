# Project: Three-Deck Card Game Architecture (V5.2 - Boss Battle)

## 1. Core Vision
A single-player virtual card game centered around a **Three-Deck System**. The project utilizes a strict Model-View-Controller (MVC) pattern. This version implements a persistent "Boss" enemy with a fixed health pool, serving as the final logic milestone for the MVP.

---

## 2. Technical Architecture

### **The Resolution Engine** (`game_state.py`)
The Controller utilizes **Category-based logic** to resolve effects:
* **The Model (`GameState`)**: 
    - Tracks `player.life_total` (starts at 20).
    - Tracks `state.energy` (resets to 5 each turn).
    - Tracks `state.current_enemy_health` (starts at 30).
* **Category Logic**: 
    - **Attack**: Subtracts `current_value` from `current_enemy_health`.
    - **Healing**: Adds `current_value` to `player.life_total` (Player cards only).
    - **Resource**: Adds `current_value` to `state.energy`.

### **The Component Structure**
* **The Controller (`GameController`)**: Manages the persistent enemy state. It ensures that encounter cards only deal damage to the player and do not reset or heal the enemy health bar.
* **The View (`cli_interface.py`)**: Renders the dual health bars and monitors for the Victory condition.

---

## 3. High-Level Game Flow (The Boss Loop)

1.  **Initialization**: `game_factory.py` sets the enemy health to 30.
2.  **Player Phase**: Player uses Attack cards to reduce the enemy's 30 HP.
3.  **Enemy Phase**: A card is drawn from the Encounter deck. Its value is subtracted directly from the player's health. The enemy's health remains persistent across turns.
4.  **Game End Conditions**:
    * **Victory**: `state.current_enemy_health <= 0`.
    * **Defeat**: `player.life_total <= 0`.