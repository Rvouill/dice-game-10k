# Main Program for Dice 10K
import tkinter as tk
from ui.game_ui import DiceGameUI

if __name__ == "__main__":
    root = tk.Tk()
    game_ui = DiceGameUI(root)
    root.mainloop()