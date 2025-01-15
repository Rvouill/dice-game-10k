# Main Program for Dice 10K
import tkinter as tk
from dice_game_10k import DiceGame10K

if __name__ == "__main__":
    root = tk.Tk()
    game = DiceGame10K(root)
    root.mainloop()