# Dice 10K #
############

# Includes
import functions
import random
import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Start #
#########

class Dice10K:
    def __init__(self, root):

        # Basic initialization of app window
        self.root = root
        self.root.title("Dice Game 10K")
        
        # Create a frame for the dice display
        self.dice_frame = tk.Frame(self.root)
        self.dice_frame.pack(pady=40)
        self.dice_frame.pack(padx=140)

        self.set_players()  

    def set_players(self):

        # Input for number of player
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)
        tk.Label(self.input_frame, text="Number of players:").pack(side=tk.LEFT, padx=5)
        self.num_players_entry = tk.Entry(self.input_frame, width=5)
        self.num_players_entry.pack(side=tk.LEFT, padx=5)
        self.num_players_entry.insert(0, "2")  # Default to 2 players

        # Start button
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)
   
    def start_game(self):
        try:
            # Retrieve and validate the number of players
            num_players = int(self.num_players_entry.get())
            if num_players < 1:
                raise ValueError("Number of players must be at least 1.")
            
            # Initialize the score table: a list of empty lists, one for each player
            self.score_table = [[] for _ in range(num_players)]
            
            # Debug: Print score table initialization
            print(f"Score table initialized for {num_players} players: {self.score_table}")

            # Clear any existing game-related UI if necessary
            if hasattr(self, 'dice_frame'):
                self.dice_frame.destroy()  
            if hasattr(self, 'input_frame'):
                self.input_frame.destroy() 
            if hasattr(self, 'start_button'):
                self.start_button.destroy() 
            
            # Create a new frame for dice-related UI
            self.dice_frame = tk.Frame(self.root)
            self.dice_frame.pack(pady=20)

            # Render Game Interface
            self.display_game()
            
            # Start Game Notification Message
            tk.messagebox.showinfo("Game Start", f"The game has started with {num_players} players!")


        except ValueError as e:
            # Handle invalid input for number of players
            tk.messagebox.showerror("Invalid Input", f"Invalid number of players: {e}")

    def display_game(self):

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
        self.num_dice_entry.insert(0, "6")  # Default to 6 dice
        
        # Roll button
        self.roll_button = tk.Button(self.root, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack(pady=40)

         # Score button
        self.scores_button = tk.Button(self.root, text="Scores", command=self.display_scores)
        self.scores_button.pack(padx=60)

        # End button
        self.end_button = tk.Button(self.root, text="End Game", command=self.end_game)
        self.end_button.pack(pady=40)

    def roll_dice(self):
        # Simulate rolling dice from functions
        results = functions.throw(int(self.num_dice_entry.get()))
        self.message_result.config(text=functions.get_results(results))

        # Update dice labels with results as image
        for label, result in zip(self.dice_labels, results):
            label.config(image=self.dice_images[result - 1])

    def display_scores(self):
         # Clear existing score display, if any
        if hasattr(self, 'score_frame'):
            self.score_frame.destroy()

        # Create a new frame for score display
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(pady=20)

        # Create a heading for the score table
        tk.Label(self.score_frame, text="Score Table", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Display the scores for each player
        for i, player_scores in enumerate(self.score_table, start=1):
            scores_text = ", ".join(map(str, player_scores)) if player_scores else "No throws yet"
            tk.Label(
                self.score_frame,
                text=f"Player {i}: {scores_text}",
                font=("Helvetica", 12),
                anchor="w"
            ).pack(fill=tk.X, padx=20, pady=5)

    def end_game(self):

        # Avoid Score Table Initialization Error
        if not self.score_table:
            tk.messagebox.showwarning("End Game", "No game in progress or no scores recorded.")
            return

        # Calculate the total score for each player
        player_totals = [sum(scores) for scores in self.score_table]

        # Determine the winner(s)
        highest_score = max(player_totals)
        winners = [i + 1 for i, score in enumerate(player_totals) if score == highest_score]

        # Generate the result message
        if len(winners) > 1:
            winner_message = f"It's a tie! Players {', '.join(map(str, winners))} win with {highest_score} points."
        else:
            winner_message = f"Player {winners[0]} wins with {highest_score} points!"

        # Display the results
        tk.messagebox.showinfo("Game Over", winner_message)

        # Optionally, print results to console for debugging
        print("Final Scores:")
        for i, total in enumerate(player_totals, start=1):
            print(f"Player {i}: {total} points")

        # Relaunch the program
        python = sys.executable  # Path to the current Python interpreter
        os.execl(python, python, *sys.argv)
        

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    game = Dice10K(root)
    root.mainloop()

