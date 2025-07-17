# Includes
import functions
import config
import random
import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Dice Game Class
class DiceGame10K:

    # Init
    def __init__(self, root):

        # Basic initialization of app window
        self.root = root
        self.root.title(config.APP_TITLE)
        self.root.geometry(config.WINDOW_SIZE)
        self.set_players()  
        self.current_player = 0
        self.round_score = 0
        self.temp_scores = []

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
            if num_players < 2:
                raise ValueError("Number of players must be at least 2.")
            
            # Store the number of players
            self.num_players = num_players
            print(f"[INFO] Number of players set to {num_players}")

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

        # Create a temporary scores frame for current player round
        if hasattr(self, 'points_input_frame'):
            self.points_input_frame.destroy()

        self.points_input_frame = tk.Frame(self.dice_container)
        self.points_input_frame.pack(pady=10)

        # Champ de saisie
        tk.Label(self.points_input_frame, text="Points à garder :").pack(side=tk.LEFT, padx=5)
        self.points_entry = tk.Entry(self.points_input_frame, width=10)
        self.points_entry.pack(side=tk.LEFT, padx=5)

        # Bouton Ajouter
        self.add_button = tk.Button(self.points_input_frame, text="Ajouter", command=self.add_points)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Bouton Valider
        self.save_button = tk.Button(self.points_input_frame, text="Valider", command=self.validate_points)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Bouton Annuler
        self.cancel_button = tk.Button(self.points_input_frame, text="Annuler", command=self.cancel_points)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

         # Label pour afficher le score temporaire
        if hasattr(self, 'round_score_label'):
            self.round_score_label.destroy()

        self.round_score_label = tk.Label(self.dice_container, text=f"Score temporaire : {self.round_score}", font=("Helvetica", 12, "bold"))
        self.round_score_label.pack(pady=5)

        print(f"[INFO] Joueur {self.current_player + 1} a lancé les dés : {results}")

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

    def update_round_score_display(self):
        if hasattr(self, 'round_score_label'):
            self.round_score_label.config(text=f"Score temporaire : {self.round_score}")

    def add_points(self):
        try:
            points = int(self.points_entry.get())
            self.round_score += points
            self.update_round_score_display()
            print(f"[AJOUT] +{points} points ajoutés au score temporaire => Total : {self.round_score}")
        except ValueError:
            tk.messagebox.showerror("Erreur", "Veuillez saisir un nombre entier de points.")

    def cancel_points(self):
        print(f"[ANNULATION] Score temporaire remis à zéro (était : {self.round_score})")
        self.round_score = 0
        self.update_round_score_display()

    def validate_points(self):
        # Ajoute le score de la manche dans le tableau de scores définitif
        self.score_table[self.current_player].append(self.round_score)

        print(f"[VALIDATION] Joueur {self.current_player + 1} a validé {self.round_score} pts.")
        print(f"[TABLE SCORE] => {self.score_table}")

        # Réinitialise le score temporaire
        self.round_score = 0
        self.update_round_score_display()

        # Supprime le champ de saisie
        self.points_input_frame.destroy()   

        # Passer au joueur suivant
        self.current_player += 1

        # Si tous les joueurs ont joué, recommencer depuis le premier
        if self.current_player >= self.num_players:
            self.current_player = 0
            print("[MANCHE TERMINÉE] Nouvelle manche à venir.")

        # Message de tour
        tk.messagebox.showinfo("Tour Suivant", f"Au tour du joueur {self.current_player + 1} !")

        # Réinitialiser le champ pour un nouveau lancé
        self.clear_game_input()

    def clear_game_input(self):
        """Réinitialise les entrées pour un nouveau tour"""
        self.num_dice_entry.delete(0, tk.END)
        self.num_dice_entry.insert(0, "6")  # Valeur par défaut
        self.message_result.config(text="")  # Nettoyer le message précédent

        # Nettoyer les images des dés
        for label in self.dice_labels:
            label.config(image="")

        # Nettoyer le champ de points s'il existe
        if hasattr(self, 'points_input_frame'):
            self.points_input_frame.destroy()

        print(f"[TOUR] Préparation du tour pour le joueur {self.current_player + 1}")