from typing import List, Dict, Any

class GameLogic:
    """
    Classe gérant la logique du jeu (sans interface).
    """

    def __init__(self, num_players: int):
        """
        Initialise la logique du jeu.

        Args:
            num_players (int): Nombre de joueurs.
        """
        self.current_player = 0
        self.round_score = 0
        self.kept_dice = []  # Dés conservés par le joueur
        self.remaining_dice = 6  # Nombre de dés restants à lancer
        self.score_table = [[] for _ in range(num_players)]
        self.num_players = num_players
        self.turn_history = []  # Historique des scores validés

    def roll_dice(self, num_dice: int) -> List[int]:
        """
        Simule un lancer de dés.

        Args:
            num_dice (int): Nombre de dés à lancer.

        Returns:
            List[int]: Résultats du lancer.
        """
        import random
        return [random.randint(1, 6) for _ in range(num_dice)]

    def select_scoring_option(self, option: Dict[str, Any]):
        """
        Gère la sélection d'une combinaison de score.

        Args:
            option (Dict[str, Any]): Option de scoring sélectionnée.
        """
        self.round_score += option["score"]
        self.kept_dice.extend(option["dice"])
        self.remaining_dice = len(option["remaining_dice"])
        return self.remaining_dice

    def validate_turn(self):
        """Valide le tour du joueur et passe au suivant."""
        self.score_table[self.current_player].append(self.round_score)
        self.round_score = 0
        self.kept_dice = []
        self.remaining_dice = 6
        self.current_player = (self.current_player + 1) % self.num_players

    def bust(self):
        """Réinitialise le score temporaire et passe au joueur suivant."""
        self.round_score = 0
        self.kept_dice = []
        self.remaining_dice = 6
        self.current_player = (self.current_player + 1) % self.num_players

    def get_total_score(self, player_index: int) -> int:
        """
        Retourne le score total d'un joueur.

        Args:
            player_index (int): Index du joueur.

        Returns:
            int: Score total.
        """
        return sum(self.score_table[player_index])