# Project: Three-Deck Card Game - Progress & Next Steps

## ✅ Completed Recently
- [x] Refactored project into a modular `src/` structure.
- [x] Finalized `Card`, `Deck`, and `Player` classes.
- [x] Implemented "Separated Architecture": Created `GameState` (Data) and `GameController` (Logic).
- [x] Established Git Branching workflow on `feature-game-loop`.
- [x] Streamlined `ARCHITECTURE.md` to reflect the new modular design.

## 🚀 Next Session: The Alpha Game Loop (`main.py`)
- [ ] **Infrastructure & Setup:**
    - [ ] Create `main.py` and import all classes from `src`.
    - [ ] Create a "Dummy Card Factory" function to generate test cards for all three decks.
    - [ ] Initialize the `GameState` (with the 3 decks and Player) and the `GameController`.
- [ ] **The Heartbeat (Interactive Loop):**
    - [ ] Implement a `while not game_over` loop.
    - [ ] **Display Phase:** Print a clear UI showing Health, Energy, Hand, and Deck counts.
    - [ ] **Input Phase:** Capture user strings (e.g., "d" to draw, "p 0" to play the first card).
- [ ] **Action Resolution:**
    - [ ] Link "draw" command to `controller.start_turn()`.
    - [ ] Build basic parsing for playing a card: call the controller to remove the card from hand and move it to the correct discard pile.
    - [ ] Verify deck cycling (shuffling back in) triggers correctly when the loop is running.

## 💡 Notes for Today
- **Focus on Connectivity:** The goal today isn't to make the game "fun" yet, but to prove that the Loop can talk to the Controller, and the Controller can update the State.
- **Verification:** Use print statements liberally to confirm that the numbers (Energy/Hand count) change exactly when you expect them to.