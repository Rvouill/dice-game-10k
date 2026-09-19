import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from typing import Dict, Any, List
import functions
import config
import os
import sys

from game.game_logic import GameLogic

class DiceGameUI:
    """
    Classe gérant l'interface utilisateur du jeu.
    """

    def __init__(self, root):
        """
        Initialise l'interface utilisateur.

        Args:
            root (tk.Tk): Fenêtre principale Tkinter.
        """
        self.root = root
        self.game_logic = None
        self.setup_ui()

    def setup_ui(self):
        """Initialise l'interface utilisateur."""
        self.root.title(config.APP_TITLE)
        self.root.geometry(config.WINDOW_SIZE)
        self.set_players()

        # Initialize game state variables
        self.selected_combinations = []  # Liste des combinaisons sélectionnées
        self.disabled_options = set()    # Ensemble des options désactivées 

    def set_players(self):
        """Affiche l'écran de configuration du nombre de joueurs."""
        # Create a container frame for Players screen
        self.screen_players = tk.Frame(self.root, width=300, height=100)
        self.screen_players.pack(pady=10)
        self.screen_players.pack_propagate(False)

        # Input for number of players
        self.input_frame = tk.Frame(self.screen_players)
        self.input_frame.pack(pady=10)
        tk.Label(self.input_frame, text="Number of players:").pack(side=tk.LEFT, padx=5)
        self.num_players_entry = tk.Entry(self.input_frame, width=5)
        self.num_players_entry.pack(side=tk.LEFT, padx=5)
        self.num_players_entry.insert(0, "2")

        # Start Game button
        self.start_button = tk.Button(
            self.screen_players,
            text="Start Game",
            command=self.start_game
        )
        self.start_button.pack(pady=10)

    def start_game(self):
        """Démarre la partie avec le nombre de joueurs spécifié."""
        try:
            num_players = int(self.num_players_entry.get())
            if num_players < 2:
                raise ValueError("Number of players must be at least 2.")

            self.num_players = num_players
            print(f"[INFO] Number of players set to {num_players}")

            # Initialiser la logique du jeu
            self.game_logic = GameLogic(num_players)

            # Initialiser le tableau de scores
            self.score_table = self.game_logic.score_table

            # Nettoyer l'écran de configuration
            if hasattr(self, 'screen_players'):
                self.screen_players.destroy()

            tk.messagebox.showinfo("Game Start", f"The game has started with {num_players} players!")

            # Afficher l'interface de jeu
            self.display_game()

        except ValueError as e:
            tk.messagebox.showerror("Invalid Input", f"Invalid number of players: {e}")

    def display_game(self):
        """Initialise et affiche l'interface principale du jeu."""
        # Create a new frame for Game User Interface
        self.screen_game = tk.Frame(self.root, width=500, height=800)
        self.screen_game.pack(pady=10)

        # Create a sub-container for input
        self.input_container = tk.Frame(self.screen_game, width=200, height=200)
        self.input_container.pack_propagate(False)
        self.input_container.pack(pady=10)

        # Input for number of dice
        tk.Label(self.input_container, text="Number of dice:").pack(pady=10)
        self.num_dice_entry = tk.Entry(self.input_container, width=5)
        self.num_dice_entry.pack(pady=10)
        self.num_dice_entry.insert(0, "6")

        # Roll button
        self.roll_button = tk.Button(
            self.input_container,
            text="Roll Dice",
            command=self.roll_dice
        )
        self.roll_button.pack(pady=10)

        # Dice container
        self.dice_container = tk.Frame(self.screen_game, width=500, height=200)
        self.dice_container.pack(pady=10)

        # Sub-container for dice images
        self.dice_labels_container = tk.Frame(self.dice_container, width=500, height=200)
        self.dice_labels_container.pack()

        # Load dice face images
        self.dice_images = []
        for i in range(1, 7):
            image = Image.open(f"assets/dice/dice-{i}.gif")
            resized_image = image.resize((60, 60))
            self.dice_images.append(ImageTk.PhotoImage(resized_image))

        # Create labels for dice
        self.dice_labels = []
        for _ in range(6):
            label = tk.Label(self.dice_labels_container)
            label.pack(side=tk.LEFT, pady=10)
            self.dice_labels.append(label)

        # Message label
        self.message_result = tk.Label(
            self.dice_container,
            text="",
            fg="yellow",
            font=("Helvetica", 12)
        )
        self.message_result.pack(pady=40)

        # Temporary score label
        self.round_score_label = tk.Label(
            self.screen_game,
            text=f"Score temporaire : {self.game_logic.round_score}",
            font=("Helvetica", 12, "bold")
        )
        self.round_score_label.pack(pady=10)

        # Validate turn button
        self.validate_turn_button = tk.Button(
            self.screen_game,
            text="Valider le tour",
            command=self.validate_turn,
            state=tk.DISABLED  # Désactivé au début (activé après une sélection)
        )
        self.validate_turn_button.pack(pady=10)

        # Scores button
        self.scores_button = tk.Button(
            self.root,
            text="Scores",
            command=self.display_scores
        )
        self.scores_button.pack(pady=10)

        # End game button
        self.end_button = tk.Button(
            self.root,
            text="End Game",
            command=self.end_game
        )
        self.end_button.pack(pady=10)

    def roll_dice(self):
        """Lance les dés et affiche les résultats."""
        print("[DEBUG] roll_dice appelé")

        # Désactiver les boutons pendant le traitement
        self.roll_button.config(state=tk.DISABLED)
        self.validate_turn_button.config(state=tk.DISABLED)

        # Réinitialiser les sélections
        self.selected_combinations = []
        self.disabled_options = set()

        # Supprimer les anciens labels de dés
        for label in self.dice_labels:
            label.destroy()
        self.dice_labels = []

        # Lancer les dés
        num_dice = self.game_logic.remaining_dice
        results = self.game_logic.roll_dice(num_dice)
        print(f"[DEBUG] Résultats du lancer : {results}")
        self.last_roll_results = results  # Stocker les résultats pour highlight_selected_dice

        # Afficher les dés
        for result in results:
            label = tk.Label(self.dice_labels_container, image=self.dice_images[result - 1])
            label.pack(side=tk.LEFT, pady=10)
            self.dice_labels.append(label)

        # Calculer les options de scoring
        self.current_scoring_options = functions.get_scoring_options(results)
        print(f"[DEBUG] Options de scoring : {self.current_scoring_options}")

        # Vérifier si c'est un BUST
        if not self.current_scoring_options:
            self.bust()
            return

        # Afficher les options de scoring
        self.display_scoring_options()
        self.message_result.config(text="Choisissez une combinaison")

        # Réactiver le bouton "Roll Dice" (mais pas "Valider le tour" tant qu'aucune combinaison n'est sélectionnée)
        self.roll_button.config(state=tk.NORMAL)

    def display_scoring_options(self):
        """Affiche les options de scoring comme des boutons, en désactivant les incompatibles."""
        if hasattr(self, 'scoring_options_frame'):
            self.scoring_options_frame.destroy()

        self.scoring_options_frame = tk.Frame(self.dice_container)
        self.scoring_options_frame.pack(pady=10)

        # Dés déjà sélectionnés (tous les dés des combinaisons sélectionnées)
        selected_dice = []
        for combo in self.selected_combinations:
            selected_dice.extend(combo["dice"])

        for option in self.current_scoring_options:
            # Vérifier si cette option utilise des dés déjà sélectionnés
            conflict = any(die in selected_dice for die in option["dice"])

            # Désactiver l'option si elle est en conflit
            state = tk.DISABLED if conflict or option in self.selected_combinations else tk.NORMAL

            # Créer le bouton
            btn = tk.Button(
                self.scoring_options_frame,
                text=f"{option['name']} (+{option['score']} pts)",
                command=lambda opt=option: self.toggle_combination(opt),
                width=30,
                anchor="w",
                state=state,
                bg="lightgreen" if option in self.selected_combinations else "SystemButtonFace"
            )
            btn.pack(pady=5, padx=10, fill="x")

    def toggle_combination(self, option: Dict[str, Any]):
        """
        Sélectionne ou désélectionne une combinaison.
        Met à jour le nombre de dés restants.
        """
        # Vérifier si la combinaison est déjà sélectionnée
        if option in self.selected_combinations:
            # Désélectionner la combinaison
            self.selected_combinations.remove(option)
            self.game_logic.round_score -= option["score"]
        else:
            # Sélectionner la combinaison
            self.selected_combinations.append(option)
            self.game_logic.round_score += option["score"]

        self.update_round_score_display()

        # Recalculer les dés restants
        all_dice = self.last_roll_results.copy()
        selected_dice = []
        for combo in self.selected_combinations:
            selected_dice.extend(combo["dice"])

        remaining_dice = [d for d in all_dice if d not in selected_dice]
        self.game_logic.remaining_dice = len(remaining_dice)

        # Mettre à jour le champ "Number of dice"
        self.num_dice_entry.delete(0, tk.END)
        self.num_dice_entry.insert(0, str(self.game_logic.remaining_dice))

        # Mettre à jour l'affichage des options
        self.display_scoring_options()

        # Mettre à jour l'affichage des dés
        self.highlight_selected_dice()

        # Activer les boutons "Valider le tour" et "Roll Dice" si au moins une combinaison est sélectionnée
        if self.selected_combinations:
            self.validate_turn_button.config(state=tk.NORMAL)
            self.roll_button.config(state=tk.NORMAL)
        else:
            self.validate_turn_button.config(state=tk.DISABLED)
            self.roll_button.config(state=tk.DISABLED)

    def highlight_selected_dice(self):
        """Met en évidence les dés des combinaisons sélectionnées."""
        # Réinitialiser tous les dés
        for label in self.dice_labels:
            label.config(bg="SystemButtonFace", bd=0)

        # Dés sélectionnés (tous les dés des combinaisons sélectionnées)
        selected_dice = []
        for combo in self.selected_combinations:
            selected_dice.extend(combo["dice"])

        # Mettre en vert les dés sélectionnés
        for label, die_value in zip(self.dice_labels, self.last_roll_results):
            if die_value in selected_dice:
                label.config(bg="lightgreen", bd=2, relief=tk.SOLID)
                selected_dice.remove(die_value)  # Éviter les doublons

    def select_scoring_option(self, option: Dict[str, Any]):
        """Gère la sélection d'une combinaison de score."""
        print(f"[DEBUG] Option sélectionnée : {option}")

        # Mettre à jour la logique du jeu
        remaining_dice = self.game_logic.select_scoring_option(option)

        # Mettre à jour l'affichage du score temporaire
        self.round_score_label.config(text=f"Score temporaire : {self.game_logic.round_score}")

        # Mettre à jour le nombre de dés à lancer
        self.num_dice_entry.delete(0, tk.END)
        self.num_dice_entry.insert(0, str(remaining_dice))

        # Supprimer les options de scoring
        if hasattr(self, 'scoring_options_frame'):
            self.scoring_options_frame.destroy()

        # Afficher un message
        if remaining_dice > 0:
            self.message_result.config(
                text=f"Dés conservés : {self.game_logic.kept_dice}. {remaining_dice} dés restants à relancer."
            )
        else:
            self.message_result.config(text="Tout roule ! Cliquez sur 'Roll Dice' pour relancer les 6 dés.")

        # Activer le bouton "Valider le tour"
        self.validate_turn_button.config(state=tk.NORMAL)

    def update_round_score_display(self):
        """Met à jour l'affichage du score temporaire."""
        if hasattr(self, 'round_score_label'):
            self.round_score_label.config(
                text=f"Score temporaire : {self.game_logic.round_score}"
            )

    def validate_turn(self):
        """Valide le tour du joueur avec les combinaisons sélectionnées."""
        if not self.selected_combinations:
            tk.messagebox.showwarning("Aucune sélection", "Veuillez sélectionner au moins une combinaison.")
            return

        # Ajouter le score à l'historique
        player_name = f"Joueur {self.game_logic.current_player + 1}"
        total_selected_score = sum(opt["score"] for opt in self.selected_combinations)
        self.game_logic.turn_history.append(f"{player_name}: +{total_selected_score} pts")

        # Valider le tour dans la logique du jeu
        self.game_logic.score_table[self.game_logic.current_player].append(total_selected_score)
        self.game_logic.round_score = 0  # <-- Réinitialiser le score temporaire
        self.game_logic.kept_dice = []
        self.game_logic.remaining_dice = 6

        # Passer au joueur suivant
        self.game_logic.current_player = (self.game_logic.current_player + 1) % self.game_logic.num_players

        # Réinitialiser les sélections
        self.selected_combinations = []
        self.disabled_options = set()

        # Réinitialiser l'interface
        self.clear_game_input()

        # Mettre à jour l'affichage du score temporaire
        self.update_round_score_display()  # <-- Met à jour l'affichage

        # Désactiver le bouton "Valider le tour"
        self.validate_turn_button.config(state=tk.DISABLED)

        # Afficher un message
        tk.messagebox.showinfo("Tour validé", f"Tour validé. Au joueur {self.game_logic.current_player + 1} !")

    def bust(self):
        """Gère le cas où le joueur est BUSTED."""
        print("[BUST] Aucune combinaison valide. Tour terminé.")

        # Réinitialiser le score temporaire
        self.game_logic.round_score = 0  # <-- Réinitialiser le score temporaire
        self.update_round_score_display()  # <-- Met à jour l'affichage

        # Réinitialiser les dés conservés
        self.game_logic.kept_dice = []
        self.game_logic.remaining_dice = 6

        # Supprimer les options de scoring
        if hasattr(self, 'scoring_options_frame'):
            self.scoring_options_frame.destroy()

        # Désactiver les boutons de jeu
        self.roll_button.config(state=tk.DISABLED)
        self.validate_turn_button.config(state=tk.DISABLED)

        # Passer au joueur suivant
        self.game_logic.current_player = (self.game_logic.current_player + 1) % self.game_logic.num_players

        # Afficher un message
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

    def confirm_bust(self):
        """Confirme le BUST et passe au joueur suivant."""
        # Réactiver les boutons
        self.roll_button.config(state=tk.NORMAL)

        # Supprimer le bouton "OK"
        if hasattr(self, 'bust_ok_button'):
            self.bust_ok_button.destroy()

        # Afficher un message
        self.message_result.config(text=f"Tour du joueur {self.game_logic.current_player + 1}.")
        tk.messagebox.showinfo(
            "BUST",
            f"Joueur {self.game_logic.current_player + 1}, à vous de jouer !"
        )

    def clear_game_input(self):
        """Réinitialise les entrées pour un nouveau tour."""
        self.num_dice_entry.delete(0, tk.END)
        self.num_dice_entry.insert(0, "6")
        self.message_result.config(text="")

        # Réinitialiser les sélections
        self.selected_combinations = []
        self.disabled_options = set()

        # Nettoyer les images des dés
        for label in self.dice_labels:
            label.config(image="", bg="SystemButtonFace", bd=0)

        # Nettoyer les options de scoring
        if hasattr(self, 'scoring_options_frame'):
            self.scoring_options_frame.destroy()

        # Désactiver le bouton "Valider le tour"
        self.validate_turn_button.config(state=tk.DISABLED)

    def display_scores(self):
        """Affiche le tableau des scores des joueurs."""
        if hasattr(self, 'score_frame'):
            self.score_frame.destroy()

        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(pady=20)

        tk.Label(
            self.score_frame,
            text="Score Table",
            font=("Helvetica", 14, "bold")
        ).pack(pady=10)

        for i, player_scores in enumerate(self.game_logic.score_table, start=1):
            scores_text = ", ".join(map(str, player_scores)) if player_scores else "No throws yet"
            tk.Label(
                self.score_frame,
                text=f"Player {i}: {scores_text}",
                font=("Helvetica", 12),
                anchor="w"
            ).pack(fill=tk.X, padx=20, pady=5)

    def end_game(self):
        """Termine la partie et affiche le gagnant."""
        if not self.game_logic.score_table:
            tk.messagebox.showwarning("End Game", "No game in progress or no scores recorded.")
            return

        player_totals = [sum(scores) for scores in self.game_logic.score_table]
        highest_score = max(player_totals)
        winners = [i + 1 for i, score in enumerate(player_totals) if score == highest_score]

        if len(winners) > 1:
            winner_message = f"It's a tie! Players {', '.join(map(str, winners))} win with {highest_score} points."
        else:
            winner_message = f"Player {winners[0]} wins with {highest_score} points!"

        tk.messagebox.showinfo("Game Over", winner_message)

        print("Final Scores:")
        for i, total in enumerate(player_totals, start=1):
            print(f"Player {i}: {total} points")

        # Relancer le programme
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def update_turn_history_display(self):
        """Met à jour l'affichage de l'historique des tours."""
        if hasattr(self, 'history_label'):
            self.history_label.config(text=" | ".join(self.game_logic.turn_history[-5:]))
        else:
            self.history_label = tk.Label(
                self.screen_game,
                text=" | ".join(self.game_logic.turn_history),
                font=("Helvetica", 10),
                wraplength=500
            )
            self.history_label.pack(pady=5)