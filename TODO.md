# Project: Three-Deck Card Game - Progress & Next Steps

## ✅ Completed Recently
- [x] Refactored project into a modular `src/` structure.
- [x] Finalized `Card`, `Deck`, and `Player` base classes.
- [x] Implemented "Separated Architecture": `GameState` (Data) and `GameController` (Logic).
- [x] **The Alpha Loop**: Created an interactive `main.py` that handles user commands and terminal UI.
- [x] **Input Handling**: Implemented command parsing for Drawing, Playing (by index), and Quitting.
- [x] **Git Milestone**: Pushed stable version to `feature-game-loop` branch.
- [x] **Blueprint Update**: Revised `ARCHITECTURE.md` to define the Encounter System logic and Turn Phase transitions.

## 🚀 Next Session: Encounter Logic & Turn Transitions
- [ ] **Implement Enemy Turn (GameController)**:
    - [ ] Create `resolve_enemy_turn()` to draw from the Encounter deck.
    - [ ] Apply Encounter card value as damage to `player.life_total`.
    - [ ] Ensure Encounter cards are properly moved to their specific discard pile.
- [ ] **Update Input Handling (main.py)**:
    - [ ] Add the `e` (End Turn) command to trigger the Encounter Phase.
    - [ ] Add terminal print statements to announce the Enemy's name and damage dealt.
    - [ ] Automate the call to `controller.start_turn()` after the enemy finishes.
- [ ] **Effect Resolution Expansion**:
    - [ ] Link card descriptions to actual state changes (e.g., healing or multi-draw).

## 💡 Notes for Today
- **Architecture is Key**: Maintain the "Referee" role of the `GameController`; `main.py` should only trigger logic, not calculate damage itself.
- **Turn Sequence**: By isolating `resolve_enemy_turn()`, we maintain the flexibility to change turn order later without refactoring the core logic.