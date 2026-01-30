# Project: Three-Deck Card Game - Progress & Next Steps

## ✅ Completed Recently
- [x] **Event Logging System**: Implemented `message_log` in `GameState` and `log_event` in `GameController`.
- [x] **Journalism Integration**: All major actions (drawing, playing, enemy attacks) are now recorded in the persistent log.
- [x] **UI Refactor**: `main.py` now renders "Recent Events," solving the visual "Flash Bug" fundamentally.
- [x] **Cleanup**: Removed the manual `UI PAUSE` code to allow for a smoother game flow.
- [x] **Blueprint Evolution**: Updated `ARCHITECTURE.md` to V4 (Energy Economy & Paid Draws).

## 🚀 Active Phase: Energy Economy & Paid Draws
- [ ] **Energy Buffer**: 
    - [ ] Update `GameController.start_turn()` to reset energy to **5**.
    - [ ] Remove automatic drawing from the `start_turn()` method.
- [ ] **Paid Draw Action**:
    - [ ] Implement `handle_draw_action()` in `GameController` with a **1 energy cost**.
    - [ ] Update `main.py` to call this new action when the 'd' command is used.
    - [ ] Log energy expenditure for every draw action in the message log.

## 🛠️ Future Logic & Content
- [ ] **Hand Management**: 
    - [ ] Implement a maximum hand size to prevent players from over-drawing with their increased energy.
- [ ] **Turn Flow Refactor**: 
    - [ ] Ensure that drawing cards is strictly an action and only 'e' ends the player phase.
- [ ] **Effect Resolution Expansion**:
    - [ ] Implement actual logic for "Heal" and "Shield" cards.

## 💡 Notes for Today
- **Tactical Depth**: Shifting to a 5-energy economy with a 1-energy cost for drawing forces the player to manage resources more strategically.
- **State-Driven UI**: The UI is now fully decoupled from immediate print statements; the `message_log` is the single source of truth for the game's narrative.