
# 🎲 Dice Game 10k

A dice game inspired by the classic "10 000", written in Python. 

## 📂 Project Structure

```
.
├── config.py             # Configuration and constants
├── dice_game_10k.py      # Core game logic
├── functions.py          # Utility functions (scoring, dice selection…)
├── main.py               # Main entry point (CLI interface)
└── images/               # Illustrations, examples or assets
```

## ⚙️ Installation

1. **Clone** the repository:

   ```bash
   git clone https://github.com/Rvouill/dice-game-10k.git
   cd dice-game-10k
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   > _Note: if `requirements.txt` is missing, make sure Python 3 is installed; the project uses only standard libraries._

## 🚀 Usage

### Interactive Mode

Run the game in your terminal:

```bash
python3 main.py
```

You can manually roll dice, keep dice, reroll, or stop your turn.

### Simulation

The file `dice_game_10k.py` runs simulations using automated strategies (e.g., score targets, number of dice kept…).

## 🎯 Game Rules

- Objective: reach 10,000 points.
- You must score **≥ 500** in your first turn to get on the board.
- **Base scoring**:
  - 1 = 100 pts, 5 = 50 pts
  - Three of a kind = value × 100 (e.g. 3×4 = 400)
  - Three 1s = 1000 pts  
- If all dice score, you can roll again and accumulate more points.
- A roll with no scoring dice ends the turn with 0 points gained.

## 🧩 Contributing

Contributions are welcome!

To contribute:

1. Fork the project.
2. Create a branch (`feat/my-strategy`).
3. Implement and test your feature.
4. Open a Pull Request.

## 📝 Authors

- **Rvouill** – main author ([github.com](https://github.com/Rvouill/)) 

## 📄 License

No license specified (default: “All rights reserved”).  
To make it open-source, consider adding a `LICENSE` file (MIT, Apache, etc.).

---

### Others Infos/Projects

- Application
  - ([Dice 10000 (Original)](https://play.google.com/store/apps/details?id=com.SoftwareByMatt.DiceDeluxe&hl=fr_CA)) 
  - ([Jeu de Dés : le jeu des 10000])(https://apps.apple.com/fr/app/jeu-de-d%C3%A9s-le-jeu-des-10000/id484002901)
- Various Rules 
 - ([Vuissoz Jean-Noël])(https://jnv.ch/index.php?cat=passions/jeux/de&page=10000&sm=1)

---

### ✅ To Do

- Add `requirements.txt` if needed.
- Specify an open-source license.
- Clarify rules (e.g., straight, pairs, etc.).

---

**Have fun** coding or playing! If you'd like additional examples, rule diagrams, or visuals—just ask 😊
