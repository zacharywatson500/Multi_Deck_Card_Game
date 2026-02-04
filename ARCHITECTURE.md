# Project: Three-Deck Card Game Architecture

## 1. Core Vision
A single-player virtual card game centered around a **Three-Deck System**. The project utilizes a Model-View-Controller (MVC) pattern where the Controller acts as a **Universal Resolver** for hybrid card effects.

---

## 2. Technical Architecture

### **The Resolution Engine** (`game_state.py`)
The Controller is moving from deck-based logic to **Category-based logic**:
* **Hybrid Support**: A single deck can contain multiple categories (Attack, Healing, Resource).
* **Category vs. Deck**: 
    - `card.category`: Dictates the **Effect** (math applied to life or energy).
    - `card.deck_type`: Dictates the **Discard Path** (integrity of individual piles).
* `resolve_card(index)`: Now branches based on the category to apply healing, damage, or energy generation.

### **The Brain vs. The Heart**
* **GameController (The Brain)**: Owns the "Resolution Engine" and handles all `player.life_total` and `state.energy` modifications.
* **main.py (The Heart/UI)**: A skinny wrapper that only displays the `message_log` and parses user commands.

---

## 3. High-Level Game Flow (The Alpha Loop - V4.3)

1.  **Refresh Phase**: UI renders Player stats and the `message_log`.
2.  **Input Phase**: UI captures command (e.g., `p 0`).
3.  **Resolution Phase**:
    * UI asks Controller: "Can I play this?"
    * Controller checks `category`:
        - **Healing**: Adds to Life, subtracts Energy.
        - **Attack**: Logs Damage, subtracts Energy.
        - **Resource**: Adds Energy (0 cost).
    * Controller updates the `message_log` and discards to `card.deck_type`.
4.  **Reset Phase**: Turn increments and energy resets to **5**.