# Includes
import functions
import random
import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class DiceGame10K:
    def __init__(self, root):

        # Basic initialization of app window
        self.root = root
        self.root.title("Dice Game 10K")
        self.set_players()  

    # Screen_1 : Set Number Of Players
    def set_players(self):

        # Create a container frame for Players screen
        self.screen_players = tk.Frame(self.root, width=300, height=100)  # Set width, height, and background
        self.screen_players.pack(pady=10)  # Add padding
        self.screen_players.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

        # Input for number of players
        self.input_frame = tk.Frame(self.screen_players)
        self.input_frame.pack(pady=10)
        tk.Label(self.input_frame, text="Number of players:").pack(side=tk.LEFT, padx=5)
        self.num_players_entry = tk.Entry(self.input_frame, width=5)
        self.num_players_entry.pack(side=tk.LEFT, padx=5)
        self.num_players_entry.insert(0, "2")  # Default to 2 players

        # Start Game button
        self.start_button = tk.Button(self.screen_players, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)
   
    # Screen_2 : Intit Game Interface
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

            # Clear previous screen before rendering new frame
            if hasattr(self, 'screen_players'):
                self.screen_players.destroy()  
            
            # Start Game Notification Message
            tk.messagebox.showinfo("Game Start", f"The game has started with {num_players} players!")

            # Render Game User Interface
            self.display_game()

        except ValueError as e:
            # Handle invalid input for number of players
            tk.messagebox.showerror("Invalid Input", f"Invalid number of players: {e}")

    # Render Game User Interface
    def display_game(self):

        # Create a new frame for Game User Interface
        self.screen_game = tk.Frame(self.root, width=500, height=800)
        self.screen_game.place(x=0, y=0)  # Position the main game container
        self.screen_game.pack(pady=10)    

        # Create a sub-container (frame) to hold the Label, Entry, and Button
        self.input_container = tk.Frame(self.screen_game, width=200, height=200)
        self.input_container.pack_propagate(False)  # Prevent the container from resizing to its children
        self.input_container.pack(pady=10)  # Add padding around the container

        # Input for number of dice
        tk.Label(self.input_container, text="Number of dice:").pack(pady=10)
        self.num_dice_entry = tk.Entry(self.input_container, width=5)
        self.num_dice_entry.pack(pady=10)
        self.num_dice_entry.insert(0, "6")  # Default to 6 dice

        # Roll button
        self.roll_button = tk.Button(self.input_container, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack(pady=10)

        # Create a sub-container (frame) to hold the Label, Entry, and Button
        self.dice_container = tk.Frame(self.screen_game,width=500,height=200)
        self.dice_container.pack(pady=10)  # Add padding around the container
        
        # Sub-container for the dice images
        self.dice_labels_container = tk.Frame(self.dice_container,width=500,height=200)
        self.dice_labels_container.pack()  # Pack it first to ensure the dice go above the message

        # Load dice face images
        self.dice_images = []
        for i in range(1, 7):  # Assuming dice images are named dice1.png to dice6.png
            image = Image.open(f"images/dice-{i}.gif")
            resized_image = image.resize((60, 60))  # Resize for consistent display
            self.dice_images.append(ImageTk.PhotoImage(resized_image))

        # Create labels for displaying dice results images
        self.dice_labels = []
        for i in range(6):  # Assuming six dice
            label = tk.Label(self.dice_labels_container)
            label.pack(side=tk.LEFT, pady=10)
            self.dice_labels.append(label)

        # Create label for displaying dice results message
        self.message_result = tk.Label(self.dice_container, text="", fg="yellow", font=("Helvetica", 12))
        self.message_result.pack(pady=40)    

        # Score button
        self.scores_button = tk.Button(self.root, text="Scores", command=self.display_scores)
        self.scores_button.pack(pady=10)

        # End button
        self.end_button = tk.Button(self.root, text="End Game", command=self.end_game)
        self.end_button.pack(pady=10)

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

        # Relaunch the program = Go To # Screen_1
        python = sys.executable  # Path to the current Python interpreter
        os.execl(python, python, *sys.argv)
        