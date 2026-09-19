# Includes
import functions
import config
import random
import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from typing import Dict, Any, List

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
        self.kept_dice = []  # Dés conservés par le joueur
        self.remaining_dice = 6  # Nombre de dés restants à lancer

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

        # Create button for validating the turn, initially disabled
        self.validate_turn_button = tk.Button(
            self.screen_game,
            text="Valider le tour",
            command=self.validate_turn,
            state=tk.DISABLED  # Désactivé au début (activé après un lancer valide)
        )
        self.validate_turn_button.pack(pady=10) 

        # Create label for displaying the temporary score
        self.round_score_label = tk.Label(
            self.screen_game,
            text=f"Score temporaire : {self.round_score}",
            font=("Helvetica", 12, "bold")
        )
        self.round_score_label.pack(pady=10)

        # Score button
        self.scores_button = tk.Button(self.root, text="Scores", command=self.display_scores)
        self.scores_button.pack(pady=10)

        # End button
        self.end_button = tk.Button(self.root, text="End Game", command=self.end_game)
        self.end_button.pack(pady=10)

    # Roll Dice Function
    def roll_dice(self):
        print("[DEBUG] roll_dice appelé")

        # Supprimer les anciens labels de dés
        for label in self.dice_labels:
            label.destroy()
        self.dice_labels = []

        # Lancer les dés (utiliser self.remaining_dice si disponible)
        num_dice = int(self.num_dice_entry.get())
        results = functions.throw(num_dice)
        print(f"[DEBUG] Résultats du lancer : {results}")

        # Afficher les dés
        for result in results:
            label = tk.Label(self.dice_labels_container, image=self.dice_images[result - 1])
            label.pack(side=tk.LEFT, pady=10)
            self.dice_labels.append(label)

        # Calculer les options de scoring
        self.current_scoring_options = functions.get_scoring_options(results)
        print(f"[DEBUG] Options de scoring : {self.current_scoring_options}")

        # Vérifier si c'est un BUST (aucune option valide)
        if not self.current_scoring_options:
            self.bust()
            return

        # Afficher les options de scoring
        self.display_scoring_options()
        self.message_result.config(text="Choisissez une combinaison")

        # Activer le bouton "Valider le tour" (si des points ont déjà été accumulés)
        if self.round_score > 0:
            self.validate_turn_button.config(state=tk.NORMAL)

    # Display Scoring Options
    def display_scoring_options(self):
        """Affiche les options de scoring comme des boutons."""
        # Supprimer les anciennes options
        if hasattr(self, 'scoring_options_frame'):
            self.scoring_options_frame.destroy()

        # Créer un cadre pour les options
        self.scoring_options_frame = tk.Frame(self.dice_container)
        self.scoring_options_frame.pack(pady=10)

        # Afficher chaque option comme un bouton
        for option in self.current_scoring_options:
            btn = tk.Button(
                self.scoring_options_frame,
                text=f"{option['name']} (+{option['score']} pts)",
                command=lambda opt=option: self.select_scoring_option(opt),
                width=30,
                anchor="w"
            )
            btn.pack(pady=5, padx=10, fill="x")

    # Handle Scoring Option Selection
    def select_scoring_option(self, option: Dict[str, Any]):
        """Gère la sélection d'une option de scoring."""
        print(f"[DEBUG] Option sélectionnée : {option}")

        # Ajouter le score au score temporaire
        self.round_score += option["score"]
        self.update_round_score_display()

        # Conserver les dés de l'option sélectionnée
        self.kept_dice.extend(option["dice"])
        print(f"[DEBUG] Dés conservés : {self.kept_dice}")

        # Mettre à jour les dés restants
        self.remaining_dice = len(option["remaining_dice"])
        print(f"[DEBUG] Dés restants : {self.remaining_dice}")

        # Mettre à jour le nombre de dés à lancer dans l'entry
        self.num_dice_entry.delete(0, tk.END)
        self.num_dice_entry.insert(0, str(self.remaining_dice))

        # Supprimer les options de scoring
        if hasattr(self, 'scoring_options_frame'):
            self.scoring_options_frame.destroy()

        # Afficher un message pour indiquer que le joueur peut relancer
        if self.remaining_dice > 0:
            self.message_result.config(text=f"Dés conservés : {self.kept_dice}. {self.remaining_dice} dés restants à relancer.")
        else:
            self.message_result.config(text="Tout roule ! Cliquez sur 'Roll Dice' pour relancer les 6 dés.")

        # Activer le bouton "Tout roule" si aucun dé ne reste
        if hasattr(self, 'roll_all_button'):
            if self.remaining_dice == 0:
                self.roll_all_button.config(state=tk.NORMAL)
            else:
                self.roll_all_button.config(state=tk.DISABLED)

        # Activer le bouton "Valider le tour"
        self.validate_turn_button.config(state=tk.NORMAL)

        # Activer le bouton "Roll Dice" (au cas où il serait désactivé)
        self.roll_button.config(state=tk.NORMAL)

    # Validate Turn Function
    def validate_turn(self):
        """Valide le tour du joueur et passe au suivant."""
        print(f"[VALIDATION] Joueur {self.current_player + 1} valide son tour avec {self.round_score} pts.")

        # Ajouter le score temporaire au tableau de scores
        self.score_table[self.current_player].append(self.round_score)

        # Réinitialiser le score temporaire et les dés conservés
        self.round_score = 0
        self.kept_dice = []
        self.remaining_dice = 6
        self.update_round_score_display()

        # Passer au joueur suivant
        self.current_player += 1
        if self.current_player >= self.num_players:
            self.current_player = 0

        # Réinitialiser l'interface
        self.clear_game_input()

        # Désactiver le bouton "Valider le tour"
        self.validate_turn_button.config(state=tk.DISABLED)

        # Afficher un message
        tk.messagebox.showinfo("Tour validé", f"Tour validé. Au joueur {self.current_player + 1} !")

    # Bust Function
    def bust(self):
        """Gère le cas où le joueur est BUSTED (aucune combinaison valide)."""
        print("[BUST] Aucune combinaison valide. Tour terminé.")

        # Réinitialiser le score temporaire
        self.round_score = 0
        self.update_round_score_display()

        # Réinitialiser les dés conservés
        self.kept_dice = []
        self.remaining_dice = 6

        # Supprimer les options de scoring
        if hasattr(self, 'scoring_options_frame'):
            self.scoring_options_frame.destroy()

        # Désactiver les boutons de jeu
        self.roll_button.config(state=tk.DISABLED)
        self.validate_turn_button.config(state=tk.DISABLED)
        if hasattr(self, 'roll_all_button'):
            self.roll_all_button.config(state=tk.DISABLED)

        # Afficher un message dans l'interface
        self.message_result.config(text=f"BUST ! Aucun point pour ce tour.", fg="red")

        # Ajouter un bouton "OK" pour passer au joueur suivant
        if hasattr(self, 'bust_ok_button'):
            self.bust_ok_button.destroy()

        self.bust_ok_button = tk.Button(
            self.dice_container,
            text="OK",
            command=self.confirm_bust,
            bg="red",
            fg="white"
        )
        self.bust_ok_button.pack(pady=10)

    # Confirm Bust Function
    def confirm_bust(self):
        """Confirme le BUST et passe au joueur suivant."""
        # Réactiver les boutons
        self.roll_button.config(state=tk.NORMAL)

        # Passer au joueur suivant
        self.current_player += 1
        if self.current_player >= self.num_players:
            self.current_player = 0

        # Réinitialiser l'interface
        self.clear_game_input()

        # Supprimer le bouton "OK"
        if hasattr(self, 'bust_ok_button'):
            self.bust_ok_button.destroy()

        # Afficher un message
        self.message_result.config(text=f"Tour du joueur {self.current_player + 1}.")
        tk.messagebox.showinfo("BUST", f"Joueur {self.current_player + 1}, à vous de jouer !")

    # Display Scores Function
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

    # End Game Function
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

    # Update Round Score Display
    def update_round_score_display(self):
        if hasattr(self, 'round_score_label'):
            self.round_score_label.config(text=f"Score temporaire : {self.round_score}")

    # Cancel Points Function
    def cancel_points(self):
        """Annule le score temporaire et réinitialise les dés conservés."""
        self.round_score = 0
        self.kept_dice = []
        self.remaining_dice = 6
        self.update_round_score_display()
        print("[ANNULATION] Score temporaire et dés conservés réinitialisés.")

    # Validate Points Function
    def validate_points(self):
        """Valide le score temporaire et passe au joueur suivant."""
        # Ajouter le score de la manche au tableau de scores
        self.score_table[self.current_player].append(self.round_score)
        print(f"[VALIDATION] Joueur {self.current_player + 1} a validé {self.round_score} pts.")

        # Réinitialiser le score temporaire et les dés conservés
        self.round_score = 0
        self.kept_dice = []
        self.remaining_dice = 6
        self.update_round_score_display()

        # Supprimer les options de scoring
        if hasattr(self, 'scoring_options_frame'):
            self.scoring_options_frame.destroy()

        # Passer au joueur suivant
        self.current_player += 1
        if self.current_player >= self.num_players:
            self.current_player = 0

        # Message de tour suivant
        tk.messagebox.showinfo("Tour Suivant", f"Au tour du joueur {self.current_player + 1} !")

        # Réinitialiser l'interface pour le nouveau tour
        self.clear_game_input()

    # Clear Game Input Function
    def clear_game_input(self):
        """Réinitialise les entrées pour un nouveau tour."""
        self.num_dice_entry.delete(0, tk.END)
        self.num_dice_entry.insert(0, "6")  # Valeur par défaut
        self.message_result.config(text="")

        # Réinitialiser les dés conservés et restants
        self.kept_dice = []
        self.remaining_dice = 6

        # Nettoyer les images des dés
        for label in self.dice_labels:
            label.config(image="")

        # Nettoyer les options de scoring
        if hasattr(self, 'scoring_options_frame'):
            self.scoring_options_frame.destroy()

        # Désactiver les boutons "Valider le tour" et "Tout roule"
        self.validate_turn_button.config(state=tk.DISABLED)
        if hasattr(self, 'roll_all_button'):
            self.roll_all_button.config(state=tk.DISABLED)