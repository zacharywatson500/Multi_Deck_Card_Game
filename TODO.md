# Project: Three-Deck Card Game - Progress & Next Steps

## ✅ Completed Recently
- [x] **Encounter System**: Implemented `resolve_enemy_turn()` in the `GameController`.
- [x] **Input Expansion**: Added the `e` (End Turn) command to `main.py`.
- [x] **Phase Flow**: Integrated automatic turn resets (`start_turn`) following enemy attacks.
- [x] **Visual Hotfix**: Manually added a `UI PAUSE` using `input()` to prevent the attack message from being cleared.
- [x] **Blueprint Evolution**: Updated `ARCHITECTURE.md` to define the "Historian" and "Journalist" roles for persistent logging.

## 🚀 Active Phase: Persistence & Event Logging
- [ ] **GameState Upgrade**: 
    - [ ] Add `message_log: List[str]` to the `GameState` class.
- [ ] **Controller Journalism**:
    - [ ] Implement `log_event(message)` in `GameController` to centralize all game notifications.
    - [ ] Integrate logging into `start_turn`, `resolve_enemy_turn`, and card-playing logic.
- [ ] **UI Refactor (main.py)**:
    - [ ] Update `display_ui` to render a "Recent Events" section from the `message_log`.
    - [ ] Remove the manual `input()` pause (since information will now persist on-screen).

## 🛠️ Future Logic & Content
- [ ] **Effect Resolution Expansion**:
    - [ ] Implement logic for "Heal" and "Resource" cards that modify state beyond just energy.
- [ ] **Win/Loss Polish**: 
    - [ ] Create specialized game-over messages for different loss conditions (e.g., Death vs. Out of Cards).

## 💡 Notes for Today
- **No More Disappearing Acts**: The move to a `message_log` solves the "Flash Bug" fundamentally by making the UI state-driven rather than print-driven.
- **Structural Integrity**: Keep the `main.py` lean; it should just display what the `message_log` contains.