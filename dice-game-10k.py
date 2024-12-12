# Dice 10K #
############

# Includes
import functions
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Start #
#########

class Dice10K:
    def __init__(self, root):
        self.root = root
        self.root.title("Dice Game 10K")
        
        # Create a frame for the dice display
        self.dice_frame = tk.Frame(self.root)
        self.dice_frame.pack(pady=40)
        self.dice_frame.pack(padx=140)

        # Load dice face images
        self.dice_images = []
        for i in range(1, 7):  # Assuming dice images are named dice1.png to dice6.png
            image = Image.open(f"images/dice-{i}.gif")
            resized_image = image.resize((60, 60))  # Resize for consistent display
            self.dice_images.append(ImageTk.PhotoImage(resized_image))

        # Create labels for displaying dice results images
        self.dice_labels = []
        for i in range(6):  # Assuming six dice
            label = tk.Label(self.dice_frame)
            label.pack(side=tk.LEFT, padx=10)
            self.dice_labels.append(label)

        # Create label for displaying dice results message
        self.message_result = tk.Label(self.root, text="", fg="yellow", font=("Helvetica", 12))
        self.message_result.pack(pady=10)

        # Input for number of dice
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)
        tk.Label(self.input_frame, text="Number of dice:").pack(side=tk.LEFT, padx=5)
        self.num_dice_entry = tk.Entry(self.input_frame, width=5)
        self.num_dice_entry.pack(side=tk.LEFT, padx=5)
        self.num_dice_entry.insert(0, "2")  # Default to 2 dice
        
        # Roll button
        self.roll_button = tk.Button(self.root, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack(pady=40)

    def roll_dice(self):
        # Simulate rolling dice from functions
        results = functions.throw(int(self.num_dice_entry.get()))
        self.message_result.config(text=functions.get_results(results))

        # Update dice labels with results (or images in the future)
        for label, result in zip(self.dice_labels, results):
            label.config(image=self.dice_images[result - 1])

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    game = Dice10K(root)
    root.mainloop()

