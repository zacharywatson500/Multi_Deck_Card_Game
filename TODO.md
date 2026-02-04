# Project: Three-Deck Card Game - Progress & Next Steps

## ✅ Completed Recently
- [x] **Controller Encapsulation**: Created `can_play_card` and `resolve_card` in the Controller.
- [x] **Skinny Main**: Removed redundant energy math from `main.py`.
- [x] **Deck Integrity**: Cards correctly route to discard piles based on origin.

## 🚀 Active Phase: Hybrid Evolution
- [ ] **Card Class Update**: 
    - [ ] Add `category` attribute to the `Card` class.
- [ ] **Resolver Expansion**:
    - [ ] Update `GameController.resolve_card` to branch by `category` (Attack, Healing, Resource).
    - [ ] Implement `player.life_total` modification for "Healing" cards.
- [ ] **Hybrid Main Deck**:
    - [ ] Inject "Healing" category cards into the "Main" deck factory in `setup_game()`.

## 🛠️ Future Logic & Content
- [ ] **Effect Registry**: Refactor `if/elif` into a dictionary-based lookup (Strategy Pattern).
- [ ] **Hand Management**: Implement a maximum hand size to balance 5-energy turns.
- [ ] **Visual Interface**: Begin Pygame development once hybrids are stable.